#!/usr/bin/env python3

"""Train on the test data like champions."""

import sys
import argparse
from operator import itemgetter

from nltk.classify.maxent import MaxentClassifier

from parse_corpus import extract_wsd_problems
from run_experiment import output_one_best
import features
import read_gold

def get_training_problems(sourceword):
    fn = "../trialdata/alltrials/{0}.data".format(sourceword)
    problems = extract_wsd_problems(fn)
    return problems

def get_training_data(sourceword, target):
    """Return a list of (featureset, label) for training."""
    out = []
    ## map from id to labels
    gold_answers = read_gold.get_gold_answers(sourceword, target)
    problems = get_training_problems(sourceword)

    ## now collate them.
    for problem in problems:
        theid = problem.instance_id
        featureset = features.extract(problem)
        label = gold_answers[theid]
        out.append((featureset, label))
    return out

def main():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, nargs=1, required=True)
    parser.add_argument('--targetlang', type=str, nargs=1, required=True)
    parser.add_argument('--classifier', type=str, nargs=1, required=False)
    args = parser.parse_args()

    all_target_languages = "de es fr it nl".split()
    assert args.targetlang[0] in all_target_languages
    target = args.targetlang[0]
    sourceword = args.sourceword[0]

    gold_answers = get_gold_answers(sourceword, target)
    instances = get_training_data(sourceword, target)
    print("... training ...")
    classifier = MaxentClassifier.train(instances, trace=0, max_iter=20)
    print("LABELS", classifier.labels())

    ## with open("../eval/{0}.output".format(sourceword), "w") as outfile:
    fn = "../trialdata/alltrials/{0}.data".format(sourceword)
    problems = extract_wsd_problems(fn)
    for problem in problems:
        featureset = features.extract(problem)
        answer = classifier.classify(featureset)
        print(output_one_best(problem, target, answer))
        label = gold_answers[problem.instance_id]
        print("CORRECT" if label == answer else "WRONG")
        print("distribution was...")
        dist = classifier.prob_classify(featureset)
        for key in dist.samples():
            print(" ", key, dist.prob(key))

if __name__ == "__main__": main()
