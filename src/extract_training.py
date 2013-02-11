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

## check about all the nouns in WSJ tagset
NOUN = ['NN','NNS','NNP']
def keep_source_sentence(tagged_sentence, sourceword):
    """tagged_sentence is a list of word,tag pairs."""
    ## now check whether we have the source word as a noun...
    for word,tag in tagged_sentence:
        if tag in NOUN:
            if wnl.lemmatize(word.lower()) == sourceword:
                return True
    return False

def load_bitext(sourcefn, targetfn, sourceword):
    """Return a list of (source,target) sentence pairs."""
    pat = re.compile(r".*"+sourceword+".*", flags=re.IGNORECASE)
    out_source = []
    out_target = []
    with open(sourcefn) as infile_s, open(targetfn) as infile_t:
        for source, target in zip(infile_s, infile_t):
            if re.match(pat, source):
                out_source.append(source.strip())
                out_target.append(target.strip())
    return out_source, out_target

def tokenize_sentences(sentences):
    """Given a list of strings, tokenize each string and return a list of
    lists."""
    return [nltk.word_tokenize(sent) for sent in sentences]

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
    tt = treetagger.TreeTagger(tt_home=tt_home, language=tt_lang)
    output = tt.batch_tag(sentences)
    return [[lemma for word,tag,lemma in sent] for sent in output]

def list_has_sublist(biglist, sublist):
    size = len(sublist)
    for pos in range(len(biglist) - len(sublist) + 1):
        maybe = biglist[pos:pos+size]
        if maybe == sublist:
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, nargs=1, required=True)
    parser.add_argument('--sourcetext', type=str, nargs=1, required=True)
    parser.add_argument('--targettext', type=str, nargs=1, required=True)
    parser.add_argument('--targetlang', type=str, nargs=1, required=True)
    parser.add_argument('--taggerhome', type=str, nargs=1, required=True)
    parser.add_argument('--treetaggerhome', type=str, nargs=1, required=False,
                        default="../TreeTagger/cmd")
    args = parser.parse_args()

    sourcefn = args.sourcetext[0]
    targetfn = args.targettext[0]
    sourceword = args.sourceword[0]
    global taggerhome
    taggerhome = args.taggerhome[0]
    all_target_languages = "de es fr it nl".split()
    assert args.targetlang[0] in all_target_languages
    targetlang = args.targetlang[0]
    tt_home = args.treetaggerhome[0]

    out_fn = "../trainingdata/{0}.{1}.train".format(sourceword, targetlang)

    source_lines, target_lines = load_bitext(sourcefn, targetfn, sourceword)
    print("got source/target lines")
    source_tokenized = tokenize_sentences(source_lines)
    print("tokenized.")
    tagger = get_tagger()
    source_tagged = tagger.batch_tag(source_tokenized)
    print("tagged.")

    labels = get_possible_senses.senses(sourceword, targetlang)

    make_into_training_data = []
    candidates = zip(source_tokenized,source_tagged,source_lines,target_lines)
    make_into_training_data = list(filter(lambda TUP:
                                     keep_source_sentence(TUP[1],sourceword),
                                     candidates))
    target_tokenized_sentences = \
        tokenize_sentences([target for a,b,c,target in make_into_training_data])

    target_lemmatized_sentences = \
        batch_lemmatize_sentences(target_tokenized_sentences,
                                  targetlang,
                                  tt_home)
    for source, target_lemmatized in zip((source for a,b,source,d
                                          in make_into_training_data),
                                          target_lemmatized_sentences):
        lowered = [tok.lower() for tok in target_lemmatized]
        labels_for_sentence = []
        for label in labels:
            if list_has_sublist(lowered, label.split()):
                labels_for_sentence.append(label)
        thelabels = ",".join(labels_for_sentence)
        print("labels:", thelabels)
        with open(out_fn, "a") as outfile:
            print(source, file=outfile)
            print(thelabels, file=outfile)

if __name__ == "__main__": main()
