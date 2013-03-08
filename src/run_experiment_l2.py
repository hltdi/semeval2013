#!/usr/bin/env python3

import sys
import argparse
import nltk
import pickle

from train_extracted_level2 import get_four_friends
from train_extracted_level2 import get_level1_classifiers
from parse_corpus import extract_wsd_problems
from train_from_extracted import get_maxent_classifier
from util_run_experiment import output_one_best
from util_run_experiment import output_five_best
import features
import stanford
import util_run_experiment
import train_extracted_level2

def test_level2(sourceword,target):
    bestoutfn = "../L2output/{0}.{1}.best".format(sourceword, target)
    oofoutfn = "../L2output/{0}.{1}.oof".format(sourceword, target)
    bestoutfile = open(bestoutfn,'w')
    oofoutfile = open(oofoutfn,'w')

    level2_classifier = util_run_experiment.get_pickled_classifier(sourceword,target,'level2')
    frd1,frd2,frd3,frd4 = sorted(list(get_four_friends(target)))   ##Need 4 more features from level1.
    classfrd1,classfrd2,classfrd3,classfrd4 = get_level1_classifiers(frd1,frd2,frd3,frd4,sourceword)
    # finaldir = "../trialdata/alltrials/"
    finaldir = "../finaltest"
    problems = util_run_experiment.get_test_instances(finaldir, sourceword)    

    
    for problem in problems:
        level1_features = features.extract(problem)
        answer_frd1 = classfrd1.classify(level1_features)
        answer_frd2 = classfrd2.classify(level1_features)
        answer_frd3 = classfrd3.classify(level1_features)
        answer_frd4 = classfrd4.classify(level1_features)
        level2_features = train_extracted_level2.extend_features(level1_features,(answer_frd1,answer_frd2,answer_frd3,answer_frd4),frd1,frd2,frd3,frd4)
        level2_answer = level2_classifier.classify(level2_features)
        level2_dist = level2_classifier.prob_classify(level2_features)
        oof_answers = util_run_experiment.topfive(level2_dist)
        print(output_one_best(problem, target, level2_answer), file=bestoutfile)
        print(output_five_best(problem, target, oof_answers),
              file=oofoutfile)


def main():
    #all_words = "bank coach education execution figure job letter match mission mood movement occupation paper passage plant post pot range rest ring scene side soil strain test".split()
    all_target_languages = [sys.argv[1]]

    all_words = util_run_experiment.final_test_words
    stanford.taggerhome = '/home/liucan/stanford-postagger-2012-11-11'
    nltk.classify.megam.config_megam(bin='/usr/local/bin/megam')

    for sourceword in all_words:
        for target in all_target_languages:
            test_level2(sourceword,target)


if __name__ == "__main__": main()
