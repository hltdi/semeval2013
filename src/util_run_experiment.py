#!/usr/bin/env python3

import argparse
import pickle
from parse_corpus import extract_wsd_problems

all_target_languages = "de es fr it nl".split()
all_words = "bank coach education execution figure job letter match mission mood movement occupation paper passage plant post pot range rest ring scene side soil strain test".split()

def output_one_best(problem, target, solution):
    """Return output for a solution for the one-best."""
    return "{0}.{1} {2} :: {3};".format(problem.source_lex,
                                        target,
                                        problem.instance_id,
                                        solution)

def output_five_best(problem, target, solutions):
    """Return output for a solution for the one-best."""
    answerstr = ";".join(solutions)
    return "{0}.{1} {2} ::: {3};".format(problem.source_lex,
                                         target,
                                         problem.instance_id,
                                         answerstr)

def topfive(dist):
    """Given a distribution (the output of running prob_classify), return the
    top five labels in that distribution."""
    probs_and_labels = [(dist.prob(key), key) for key in dist.samples()]
    descending = sorted(probs_and_labels, reverse=True)
    labels = [label for (prob,label) in descending]
    return labels[:5]

def get_argparser():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, required=True)
    parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--taggerhome', type=str, required=False,
        default="/home/alex/software/stanford-postagger-2012-11-11")
    parser.add_argument('--trialdir', type=str, required=True)
    return parser

def get_test_instances(trialdir, sourceword):
    """Given a trialdir and a source word, load up all the problems that we need
    to solve."""
    fn = "{0}/{1}.data".format(trialdir, sourceword)
    return extract_wsd_problems(fn)

def get_pickled_classifier(sourceword,targetlang,level):
    if level == 'level1': path = "L1pickle"
    else:  path = "../L2pickle"
    try:
        classifier = pickle.load(
                           open( "{}/{}.{}.{}.pickle".format(path,sourceword,targetlang,level)  ,'rb')
                                  )
    except: return None #erint ("{}/{}.{}.{}.pickle".format(path,sourceword,targetlang,level))
    else:  return classifier    ##If the pickle isn't there, just return None


