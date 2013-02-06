#!/usr/bin/env python3

import sys
import argparse

from parse_corpus import extract_wsd_problems

def extract(problem):
    """Given a WSDProblem, return the features for the sentence."""
    out = {}

    targetword = problem.source_lex
    if problem.source_lex.endswith(".n"):
        targetword = problem.source_lex[:-2]

    ## 'cw' for 'contains word'. bag of word features
    for sent in problem.tokenized:
        wordfeatures = dict([('cw(%s)' % w, True) for w in sent])
        out.update(wordfeatures)

    ## 'cl' for 'contains lemma'. bag of lemma features
    for sent in problem.lemmatized:
        lemmafeatures = dict([('cl(%s)' % w, True) for w in sent])
        out.update(wordfeatures)

    ## 'w' for 'window'. surrounding words. This could be better; we should
    ## use alignments and tags here.
    WIDTH=3
    for sent in problem.lemmatized:
        indices = [i for i,w in enumerate(sent) if w == targetword]
        for index in indices:
            ## window of WIDTH before
            lowerbound = min(0, index-WIDTH)
            windowfeatures = dict([('w(%s)' % w, True)
                                  for w in sent[lowerbound:index]])
            out.update(windowfeatures)
            ## and WIDTH after
            upperbound = index+WIDTH
            windowfeatures = dict([('w(%s)' % w, True)
                                  for w in sent[index+1:upperbound+1]])
            out.update(windowfeatures)
    return out

def main():
    """Quick demo for the feature extractor."""
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, nargs=1, required=True)
    args = parser.parse_args()
    sourceword = args.sourceword[0]

    fns = ["../trialdata/alltrials/{0}.data".format(sourceword)]

    for fn in fns:
        problems = extract_wsd_problems(fn)
        for problem in problems:
            features = extract(problem)
            print(features)

if __name__ == "__main__": main()
