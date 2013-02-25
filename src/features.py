#!/usr/bin/env python3

import sys
import argparse

import nltk

from parse_corpus import extract_wsd_problems
import stanford

def extract(problem):
    """Given a WSDProblem, return the features for the sentence."""
    out = {}

    targetword = problem.source_lex
    if problem.source_lex.endswith(".n"):
        targetword = problem.source_lex[:-2]

    tokenized = nltk.tag.untag(problem.tagged)

    ## 'cw' for 'contains word'. bag of word features
    wordfeatures = dict([('cw(%s)' % w, True) for w in tokenized])
    out.update(wordfeatures)

    ## 'cl' for 'contains lemma'. bag of lemma features
    lemmafeatures = dict([('cl(%s)' % w, True) for w in problem.lemmatized])
    out.update(wordfeatures)

    ## 'w' for 'window'. surrounding words. This could be better; we should
    ## use alignments and tags here.
    WIDTH=3
    ## TODO(alexr): use the stored indices of the head word.
    for index in problem.head_indices:
        ## window of WIDTH before
        lowerbound = min(0, index-WIDTH)
        windowfeatures = dict([('w(%s)' % w, True)
                              for w in tokenized[lowerbound:index]])
        out.update(windowfeatures)
        ## and WIDTH after
        upperbound = index+WIDTH
        windowfeatures = dict([('w(%s)' % w, True)
                              for w in tokenized[index+1:upperbound+1]])
        out.update(windowfeatures)
    return out

def main():
    """Quick demo for the feature extractor."""
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, required=True)
    parser.add_argument('--taggerhome', type=str, required=True)
    args = parser.parse_args()
    sourceword = args.sourceword
    stanford.taggerhome = args.taggerhome

    fns = ["../trialdata/alltrials/{0}.data".format(sourceword)]

    for fn in fns:
        problems = extract_wsd_problems(fn)
        for problem in problems:
            print("**** PROBLEM ****")
            print(problem.tagged)
            features = extract(problem)
            print(features)

if __name__ == "__main__": main()
