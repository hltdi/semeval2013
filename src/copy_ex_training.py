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
from Aligner import sort_alignment

wnl = wordnet.WordNetLemmatizer()

taggerhome = None
@functools.lru_cache(maxsize=20)
def get_tagger():
    ## these need to be environment variables or commandline arguments.
    tagger = taggerhome + '/models/wsj-0-18-bidirectional-distsim.tagger'
    jar = taggerhome + '/stanford-postagger.jar'
    stanford_tagger = POSTagger(tagger, jar, encoding='utf8',java_options = '-mx5000m')
    ##   path_to_model, path_to_jar=None, encoding=None, verbose=False, java_options='-mx1000m'
    return stanford_tagger

## These are all the kinds of nouns present in WSJ tagsets.
NOUN = {'NN','NNS','NNP','NP','NNPS','NPS'}
def keep_candidate(candidate, sourceword):
    """Decide whether to keep a candidate based on its tagged source
    sentence."""
    ## now check whether we have the source word as a noun...
    for word,tag in candidate.source_tagged:
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
                ## if len(out_source) == 200: break
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
    return [[lemma for word,tag,lemma in sent] for sent in output]

def list_has_sublist(biglist, sublist):
    """We could use this to look for known target-language senses in the target
    text. Possibly fall back to this if we can't find a good target-language
    sense with the alignments?"""
    size = len(sublist)
    for pos in range(len(biglist) - len(sublist) + 1):
        maybe = biglist[pos:pos+size]
        if maybe == sublist:
            return True
    return False

class TrainingCandidate:
    def __init__(self, source_line, target_line, alignment_line):
        self.source_line = source_line.strip()
        self.target_line = target_line.strip()
        self.alignment_line = alignment_line.strip()

        self.target_tokenized = self.target_line.split()
        self.source_tokenized = self.source_line.split()

        # fill in later
        self.source_tagged = None
        self.target_lemmatized = None
        self.source_lemmatized = None

def batch_lemmatize(candidates, targetlang, tt_home):
    """For each candidate, lemmatize the sentences and stick that information on
    the candidate objects."""
    ## target language
    sents = [candidate.target_tokenized for candidate in candidates]
    lemmatized_sentences = batch_lemmatize_sentences(sents, targetlang, tt_home)
    assert len(lemmatized_sentences) == len(sents)
    for candidate,lemmas in zip(candidates, lemmatized_sentences):
        candidate.target_lemmatized = lemmas

    ## source language
    sents = [candidate.source_tokenized for candidate in candidates]
    lemmatized_sentences = batch_lemmatize_sentences(sents, "en", tt_home)
    assert len(lemmatized_sentences) == len(sents)
    for candidate,lemmas in zip(candidates, lemmatized_sentences):
        candidate.source_lemmatized = lemmas

def batch_source_tag(candidates):
    sents = [candidate.source_tokenized for candidate in candidates]
    tagger = get_tagger()
    tagged_sents = tagger.batch_tag(sents)
    for candidate,tagged_sent in zip(candidates, tagged_sents):
        candidate.source_tagged = tagged_sent
    print("tagged.")

def get_argparser():
    """Build the argument parser for main."""
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

def main(sourcefn,targetfn,alignmentfn,sourceword,taggerhome_pa,targetlang):
    #parser = get_argparser()
    #args = parser.parse_args()

    #sourcefn = args.sourcetext
    #targetfn = args.targettext
    #alignmentfn = args.alignments
    #sourceword = args.sourceword
    global taggerhome
    taggerhome = taggerhome_pa
    all_target_languages = "de es fr it nl".split()
    assert targetlang in all_target_languages
    #targetlang = args.targetlang
    tt_home = "../TreeTagger/cmd"  #args.treetaggerhome

    out_fn = "../trainingdata/{0}.{1}.train".format(sourceword, targetlang)

    ## load up all the preprocessed and aligned data.
    source_lines, target_lines, alignment_lines = \
        load_bitext(sourcefn, targetfn, alignmentfn, sourceword)
    print("got source/target lines")

    ## labels = get_possible_senses.senses(sourceword, targetlang)
    assert(len(source_lines) == len(target_lines) == len(alignment_lines) )

    candidates = []
    for sl, tl, al in zip(source_lines, target_lines, alignment_lines):
        candidates.append(TrainingCandidate(sl,tl,al))

    ## tag it up.
    batch_source_tag(candidates)

    ## having listed the candidates, filter them down.
    make_into_training_data = []
    for candidate in candidates:
        if keep_candidate(candidate, sourceword):
            make_into_training_data.append(candidate)

    ## lemmatize remaining candidates for both languages.
    batch_lemmatize(make_into_training_data, targetlang, tt_home)

    with open(out_fn, "w") as outfile:
        for candidate in make_into_training_data:
            labels_for_sentence = []
            lowered = [tok.lower() for tok in candidate.source_lemmatized]
            tags = [tag for (word,tag) in candidate.source_tagged]
            alignment = sort_alignment(candidate.alignment_line).split()
            tws = target_words_for_each_source_word(candidate.source_lemmatized,
                                                    candidate.target_lemmatized,
                                                    alignment)
            source_lemmas = candidate.source_lemmatized
            target_lemmas = candidate.target_lemmatized
            for i in range(len(tags)):
                if (source_lemmas[i] == sourceword and
                    tags[i] in NOUN and
                    tws[i]):
                    withtags = ["{0}/{1}".format(word,tag)
                                for word,tag in candidate.source_tagged]
                    print(" ".join(withtags), file=outfile)
                    print(i, file=outfile) ## index of source word
                    print(" ".join(tws[i]).lower(), file=outfile)

#if __name__ == "__main__": generate_all()

def generate_all():
    #main(sourcefn,targetfn,alignmentfn,sourceword,taggerhome,targetlang)
    all_target_languages = "nl de es fr it".split()
    all_words = "bank coach education execution figure job letter match mission mood movement occupation paper passage plant post pot range rest ring scene side soil strain test".split()
    all_words = "rest ring scene side soil strain test".split()#['ring']
    all_target_languages = ['it']
    sourcefn="/space/Europarl_Intersection_preprocessed/intersection.en.txt.ascii"
    #targetfn="/space/Europarl_Intersection_preprocessed/intersection."+targetlang+".txt"
    #alignmentfn="/space/output_en_"+targetlang+"/training.align"
    taggerhome="/home/liucan/stanford-postagger-2012-11-11" 
    
    for targetlang in all_target_languages:
        for sourceword in all_words:
            targetfn="/space/Europarl_Intersection_preprocessed/intersection."+targetlang+".txt"
            alignmentfn="/space/output_en_"+targetlang+"/training.align"
            main(sourcefn,targetfn,alignmentfn,sourceword,taggerhome,targetlang)
            print ("Done with:",sourceword,targetlang)


if __name__ == "__main__": generate_all()
