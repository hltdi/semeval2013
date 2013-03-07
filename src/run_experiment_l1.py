#!/usr/bin/env python3

import sys
import argparse
import nltk

import features
import stanford

import util_run_experiment
from util_run_experiment import output_one_best
from util_run_experiment import output_five_best
from util_run_experiment import all_target_languages
from util_run_experiment import all_words
from util_run_experiment import get_pickled_classifier

def main():
    parser = util_run_experiment.get_argparser()
    args = parser.parse_args()
    assert args.targetlang in all_target_languages
    assert args.sourceword in all_words

    targetlang = args.targetlang
    sourceword = args.sourceword
    trialdir = args.trialdir
    stanford.taggerhome = args.taggerhome

    print("Loading and tagging test problems...")
    problems = util_run_experiment.get_test_instances(trialdir, sourceword)
    print("OK loaded and tagged.")

    ## classifier = get_maxent_classifier(sourceword, targetlang)
    classifier = get_pickled_classifier(sourceword, targetlang, "level1")
    if not classifier:
        print("Couldn't load pickled L1 classifier?")
        return
    print("Loaded pickled L1 classifier!")


    bestoutfn = "../L1output/{0}.{1}.best".format(sourceword, targetlang)
    oofoutfn = "../L1output/{0}.{1}.oof".format(sourceword, targetlang)
    with open(bestoutfn, "w") as bestoutfile, \
         open(oofoutfn, "w") as oofoutfile:
        for problem in problems:
            featureset = features.extract(problem)
            answer = classifier.classify(featureset)
            dist = classifier.prob_classify(featureset)
            oof_answers = util_run_experiment.topfive(dist)
            print(output_one_best(problem, targetlang, answer),
                  file=bestoutfile)
            print(output_five_best(problem, targetlang, oof_answers),
                  file=oofoutfile)

if __name__ == "__main__": main()
