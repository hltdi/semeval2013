#!/usr/bin/env python3

import sys
import argparse

from parse_corpus import extract_wsd_problems


def extract(problem):
    """Given a WSDProblem, return the features for the sentence."""
    out = {}
    for sent in problem.tokenized:
        wordfeatures = dict([('cw(%s)' % w, True) for w in sent])
        out.update(wordfeatures)
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
