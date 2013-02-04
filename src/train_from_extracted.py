#!/usr/bin/env python3

"""Train on training data. This will open up a file in ../trainingdata/ and get
the sweet, sweet instances out of it. And then train on them and produce a
maxent classifier for a given target language and source word."""

import sys
import argparse
from operator import itemgetter

from nltk.classify.maxent import MaxentClassifier

from wsd_problem import WSDProblem
from parse_corpus import extract_wsd_problems
from run_experiment import output_one_best
from train_on_test import get_gold_answers
import features

def get_training_problems(sourceword):
    fn = "../trialdata/alltrials/{0}.data".format(sourceword)
    problems = extract_wsd_problems(fn)
    return problems

def get_training_data_from_extracted(sourceword, targetlang):
    """Return a list of (featureset, label) for training."""
    out = []
    problems = []
    fn = "../trainingdata/{0}.{1}.train".format(sourceword, targetlang)

    with open(fn) as infile:
        lines = infile.readlines()
        lines = [line.strip() for line in lines]
        labelss = [line.split(",") for line in lines[1::2]]
        contexts = [line for line in lines[0::2]]
        assert len(contexts) == len(labelss)

    problemid = 0
    answers = {}
    for context, labels in zip(contexts, labelss):
        for label in labels:
            if label == '': continue
            problem = WSDProblem(sourceword, 0, context, problemid)
            problems.append(problem)
            answers[problemid] = label
            problemid += 1

    for problem in problems:
        theid = problem.instance_id
        featureset = features.extract(problem)
        label = answers[theid]
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

    instances = get_training_data_from_extracted(sourceword, target)
    print("got {0} training instances!!".format(len(instances)))
    print("... training ...")
    classifier = MaxentClassifier.train(instances, trace=0, max_iter=20)
    print("LABELS", classifier.labels())

    ## with open("../eval/{0}.output".format(sourceword), "w") as outfile:
    fn = "../trialdata/alltrials/{0}.data".format(sourceword)
    problems = extract_wsd_problems(fn)
    gold_answers = get_gold_answers(sourceword, target)
    for problem in problems:
        featureset = features.extract(problem)
        answer = classifier.classify(featureset)
        print(problem.context)
        print(output_one_best(problem, target, answer))
        label = gold_answers[problem.instance_id]
        print("CORRECT" if label == answer else "WRONG", end=" ")
        print("should be:", label)

if __name__ == "__main__": main()
