#!/usr/bin/env python3

"""Train on training data. This will open up a file in ../trainingdata/ and get
the sweet, sweet instances out of it. And then train on them and produce a
maxent classifier for a given target language and source word."""

import nltk
import pickle
import sys
import argparse
from operator import itemgetter
from collections import defaultdict

from nltk.classify.maxent import MaxentClassifier

from wsd_problem import WSDProblem
from parse_corpus import extract_wsd_problems
import read_gold
import features
import stanford

def get_training_data_from_extracted(sourceword, targetlang):
    """Return a list of (featureset, label) for training."""
    out = []
    problems = []
    fn = "../trainingdata/{0}.{1}.train".format(sourceword, targetlang)

    with open(fn) as infile:
        lines = infile.readlines()
        lines = [line.strip() for line in lines]
        contexts = [line for line in lines[0::3]]
        indices = [int(line) for line in lines[1::3]]
        labelss = [line.split(",") for line in lines[2::3]]
        assert len(contexts) == len(labelss) == len(indices)

    answers = []
    for context, index, labels in zip(contexts, indices, labelss):
        problem = WSDProblem(sourceword, context,
                             testset=False, head_index=index)
        for label in labels:
            if label == '': continue
            problems.append(problem)
            answers.append(label)

    for problem,answer in zip(problems, answers):
        featureset = features.extract(problem)
        label = answer
        assert(type(label) is str)
        out.append((featureset, label))
        #print("###the features are: \n{}".format(featureset))
        #input()
    return out

def remove_onecount_instances(instances):
    """Given a list of featureset,label instances, find the ones with labels
    that only happen once. Remove them."""
    labelcounts = defaultdict(int)
    onecounts = set()
    for (featureset,label) in instances:
        labelcounts[label] += 1
    for label in labelcounts:
        if labelcounts[label] == 1:
            onecounts.add(label)
    return [(featureset,label) for (featureset,label) in instances
                               if label not in onecounts]

def get_maxent_classifier(sourceword, target):
    instances = get_training_data_from_extracted(sourceword, target)
    print("got {0} training instances!!".format(len(instances)))
    without_onecounts = remove_onecount_instances(instances)
    print("removed {0} one-count instances!!".format(
        len(instances) - len(without_onecounts)))
    instances = without_onecounts

    print("... training ...")
    classifier = MaxentClassifier.train(instances,
                                        trace=0,
                                        max_iter=20,
                                        algorithm='megam')
    print("LABELS", classifier.labels())
    return classifier

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
    nltk.classify.megam.config_megam(bin='/usr/local/bin/megam')
    classifier = get_maxent_classifier(sourceword, target)

    fn = "../trialdata/alltrials/{0}.data".format(sourceword)
    ## XXX(alexr): fix later.
    stanford.taggerhome = "/home/alex/software/stanford-postagger-2012-11-11"
    problems = extract_wsd_problems(fn)
    gold_answers = read_gold.get_gold_answers(sourceword, target)
    for problem in problems:
        featureset = features.extract(problem)
        answer = classifier.classify(featureset)
        print(problem.tokenized)
        print(answer)
        label = gold_answers[problem.instance_id]
        print("CORRECT" if label == answer else "WRONG", end=" ")
        print("should be:", label)

if __name__ == "__main__": main()
