#!/usr/bin/env python3

import sys
import argparse
import nltk

from parse_corpus import extract_wsd_problems
from train_from_extracted import get_maxent_classifier
from util_run_experiment import output_one_best
import features
import stanford

def main():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, required=True)
    parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--taggerhome', type=str, required=True)
    args = parser.parse_args()

    all_target_languages = "de es fr it nl".split()
    assert args.targetlang in all_target_languages
    targetlang = args.targetlang
    sourceword = args.sourceword
    stanford.taggerhome = args.taggerhome

    fn = "../trialdata/alltrials/{0}.data".format(sourceword)

    nltk.classify.megam.config_megam(bin='/usr/local/bin/megam')
    classifier = get_maxent_classifier(sourceword, targetlang)
    with open("../eval/{0}.output".format(sourceword), "w") as outfile:
        problems = extract_wsd_problems(fn)
        for problem in problems:
            featureset = features.extract(problem)
            answer = classifier.classify(featureset)
            print(output_one_best(problem, targetlang, answer), file=outfile)

if __name__ == "__main__": main()
