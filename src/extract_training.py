#!/usr/bin/env python3

"""Given a source word, source text and target text filenames, produce training
data files."""

import sys
import argparse
import functools
import re

import nltk
from nltk.tag.stanford import POSTagger
from nltk.stem import wordnet

import get_possible_senses
import treetagger
from Aligner import target_words_for_each_source_word

wnl = wordnet.WordNetLemmatizer()

## Given a pair of lines (src,trg) we need to decide whether this is a source
## line we're interested in, and then we need to decide what the target word
## sense is.

taggerhome = None
@functools.lru_cache(maxsize=20)
def get_tagger():
    ## these need to be environment variables or commandline arguments.
    tagger = taggerhome + '/models/wsj-0-18-bidirectional-distsim.tagger'
    jar = taggerhome + '/stanford-postagger.jar'
    stanford_tagger = POSTagger(tagger, jar, encoding='utf8')
    return stanford_tagger

## TODO(alexr): check about all the nouns in WSJ tagset
NOUN = ['NN','NNS','NNP']
def keep_source_sentence(tagged_sentence, sourceword):
    """tagged_sentence is a list of word,tag pairs."""
    ## now check whether we have the source word as a noun...
    for word,tag in tagged_sentence:
        if tag in NOUN:
            if wnl.lemmatize(word.lower()) == sourceword:
                return True
    return False

def load_bitext(sourcefn, targetfn, alignfn, sourceword):
    """Return three lists of sentence-like things. First source, then
    target, then alignment."""
    pat = re.compile(r".*"+sourceword+".*", flags=re.IGNORECASE)
    out_source = []
    out_target = []
    out_align = []
    with open(sourcefn) as infile_s, \
         open(targetfn) as infile_t, \
         open(alignfn) as infile_align:
        for source, target, alignment in zip(infile_s, infile_t, infile_align):
            if re.match(pat, source):
                out_source.append(source.strip())
                out_target.append(target.strip())
                out_align.append(alignment.strip())
                break
    return out_source, out_target, out_align

def lemmatize_sentence(sentence, language, tt_home=None):
    """For a tokenized sentence in the given language, call TreeTagger on it to
    get a list of lemmas."""
    codes_to_names = {"en":"english", "de":"german", "it":"italian",
                      "es":"spanish", "fr":"french", "nl":"dutch"}
    tt_lang = codes_to_names[language]
    tt = treetagger.TreeTagger(tt_home=tt_home, language=tt_lang)
    output = tt.tag(sentence)
    return [lemma for word,tag,lemma in output]

def batch_lemmatize_sentences(sentences, language, tt_home=None):
    """For a list of tokenized sentences in the given language, call TreeTagger
    on them to get a list of lemmas."""
    codes_to_names = {"en":"english", "de":"german", "it":"italian",
                      "es":"spanish", "fr":"french", "nl":"dutch"}
    tt_lang = codes_to_names[language]

    if tt_lang == 'english':
        tt = treetagger.TreeTagger(tt_home=tt_home,
                                   language=tt_lang,
                                   encoding='latin-1')
    else:
        tt = treetagger.TreeTagger(tt_home=tt_home, language=tt_lang)
    output = tt.batch_tag(sentences)
    ## out = []
    ## for sent in output:
    ##     thissent = []
    ##     try:
    ##         for (word,tag,lemma) in sent:
    ##             thissent.append(lemma)
    ##         out.append(thissent)
    ##     except:
    ##         for thing in sent:
    ##             print(thing, len(thing))
    ##         return out
    ## return out
    return [[lemma for word,tag,lemma in sent] for sent in output]

def list_has_sublist(biglist, sublist):
    size = len(sublist)
    for pos in range(len(biglist) - len(sublist) + 1):
        maybe = biglist[pos:pos+size]
        if maybe == sublist:
            return True
    return False

def get_parser():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, required=True)
    parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--sourcetext', type=str, required=True)
    parser.add_argument('--targettext', type=str, required=True)
    parser.add_argument('--taggerhome', type=str, required=True)
    parser.add_argument('--alignments', type=str, required=True)
    parser.add_argument('--treetaggerhome', type=str, required=False,
                        default="../TreeTagger/cmd")
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()

    sourcefn = args.sourcetext
    targetfn = args.targettext
    alignmentfn = args.alignments
    sourceword = args.sourceword
    global taggerhome
    taggerhome = args.taggerhome
    all_target_languages = "de es fr it nl".split()
    assert args.targetlang in all_target_languages
    targetlang = args.targetlang
    tt_home = args.treetaggerhome

    out_fn = "../trainingdata/{0}.{1}.train".format(sourceword, targetlang)

    ## load up all the preprocessed and aligned data.
    source_lines, target_lines, alignment_lines = \
        load_bitext(sourcefn, targetfn, alignmentfn, sourceword)
    print("got source/target lines")

    ## split on spaces and tag.
    source_tokenized = [line.strip().split() for line in source_lines]
    tagger = get_tagger()
    source_tagged = tagger.batch_tag(source_tokenized)
    print("tagged.")

    labels = get_possible_senses.senses(sourceword, targetlang)

    make_into_training_data = []
    candidates = zip(source_tokenized, source_tagged, source_lines,
                     target_lines, alignment_lines)

    ## having listed the candidates, filter them down.
    make_into_training_data = []
    for candidate in candidates:
        s_tagged = candidate[1]
        if keep_source_sentence(s_tagged, sourceword):
            make_into_training_data.append(candidate)

    ## tokenize & lemmatize remaining target-language sentences.
    target_tokenized_sentences = [target.split()
                                  for a,b,c,target,e in make_into_training_data]
    target_lemmatized_sentences = \
        batch_lemmatize_sentences(target_tokenized_sentences,
                                  targetlang,
                                  tt_home)
    source_tokenized = [tup[0] for tup in make_into_training_data]
    source_lemmatized_sentences = \
        batch_lemmatize_sentences(source_tokenized, "en", tt_home)
    alignments = [tup[4] for tup in make_into_training_data]

    for source, source_lemmatized, target_lemmatized, alignment in \
            zip(source_tokenized,
                source_lemmatized_sentences,
                target_lemmatized_sentences,
                alignments):
        lowered = [tok.lower() for tok in target_lemmatized]
        labels_for_sentence = []
        for label in labels:
            if list_has_sublist(lowered, label.split()):
                labels_for_sentence.append(label)
        thelabels = ",".join(labels_for_sentence)
        print("labels:", thelabels)
        ## TODO(alexr): only include labels that are aligned with the source
        ## word.
        tws = target_words_for_each_source_word(source,
                                                target_lemmatized,
                                                alignment.split())
        print(list(zip(source, tws)))
        with open(out_fn, "w") as outfile:
            print(" ".join(source), file=outfile)
            print(thelabels, file=outfile)

if __name__ == "__main__": main()
