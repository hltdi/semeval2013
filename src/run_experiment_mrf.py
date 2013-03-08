#!/usr/bin/env python3

import argparse
import itertools
import math
import random
import stanford

import nltk
import features

from loopybp import Edge
from loopybp import Node
from loopybp import beliefprop
from loopybp import possible_values

import util_run_experiment
from util_run_experiment import output_one_best
from util_run_experiment import output_five_best
from util_run_experiment import all_target_languages
from util_run_experiment import all_words
from util_run_experiment import get_pickled_classifier

import co_occur

classifiers = {}

cooccurrences = {}

def unary_penalty_table(classifier, featureset):
    """Take a classifier and a featureset; return a dictionary where we've
    turned the probabilities into negative logprobs."""
    dist = classifier.prob_classify(featureset)
    labels_and_probs = [(key, dist.prob(key)) for key in dist.samples()]
    ## to be really silly, scale up the unary potentials.
    return dict([(label, 10 * -math.log(prob,2))
                 for (label, prob) in labels_and_probs])

def mrf_optimize(problem):
    """Build the MRF and do the optimization!!"""
    featureset = features.extract(problem)

    for lang in all_target_languages:
        classifier = classifiers[lang]
        unary = unary_penalty_table(classifier, featureset)
        print(unary)
        langnode = Node(lang, unary)

    ## get all the combinations of nodes.
    langpairs = list(itertools.combinations(all_target_languages, 2))

    ## create an edge for each language pair.
    for l1, l2 in langpairs:
        print("building edges for", l1, l2)
        edgepotentials = {}
        for val1 in possible_values(l1):
            for val2 in possible_values(l2):
                cooccurrence = cooccurrences[(l1,l2)]
                joint = cooccurrence.lookup_joint(l1, val1, l2, val2)
                # negative logprob of the joint probability. Definitely the best
                # edge potential, for sure.
                edgepotentials[(val1,val2)] = -math.log(joint, 2)
        Edge(l1, l2, edgepotentials)

    ## XXX how many iterations?
    print("mrf solving!!!")
    answers, oof_answers = beliefprop(10)
    print("mrf solved!!!")
    return answers, oof_answers

def build_cooccurrences(sourceword):
    langpairs = list(itertools.combinations(all_target_languages, 2))
    ## create an edge for each language pair.
    for l1, l2 in langpairs:
        print("building cooccurrence", l1, l2)
        cls = co_occur.Occurrence(sourceword,l1,l2)
        cooccurrences[(l1,l2)] = cls
        ## XXX(alexr): gross, should just store it once.
        cooccurrences[(l2,l1)] = cls

def mrf_get_argparser():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, required=True)
    parser.add_argument('--taggerhome', type=str, required=False,
        default="/home/alex/software/stanford-postagger-2012-11-11")
    parser.add_argument('--trialdir', type=str, required=True)
    return parser

def main():
    parser = mrf_get_argparser()
    args = parser.parse_args()
    assert args.sourceword in all_words

    sourceword = args.sourceword
    trialdir = args.trialdir
    stanford.taggerhome = args.taggerhome

    ## load up the cooccurrences.
    print("Loading cooccurrence information.")
    build_cooccurrences(sourceword)

    for lang in all_target_languages:
        classifier = get_pickled_classifier(sourceword, lang, "level1")
        classifiers[lang] = classifier
        if not classifier:
            print("Couldn't load pickled L1 classifier?")
            return
    print("Loaded pickled L1 classifiers!")

    print("Loading and tagging test problems...")
    problems = util_run_experiment.get_test_instances(trialdir, sourceword)
    print("OK loaded and tagged.")

    outfiles = {}
    for lang in all_target_languages:
        bestoutfn = "../MRFoutput/{0}.{1}.best".format(sourceword, lang)
        oofoutfn = "../MRFoutput/{0}.{1}.oof".format(sourceword, lang)
        bestout = open(bestoutfn, "w")
        oofout = open(oofoutfn, "w")
        outfiles[lang + ".best"] = bestout
        outfiles[lang + ".oof"] = oofout

    for problem in problems:
        ## these are dictionaries.
        answers, oof_answers = mrf_optimize(problem)
        for lang in answers:
            answer = answers[lang]
            outfile = outfiles[lang + ".best"]
            print(output_one_best(problem, lang, answer), file=outfile)

            outfile = outfiles[lang + ".oof"]
            topfive = oof_answers[lang]
            print(output_five_best(problem, lang, topfive), file=outfile)

    ## now close all the outfiles.
    for key in outfiles:
        outfiles[key].close()

if __name__ == "__main__": main()
