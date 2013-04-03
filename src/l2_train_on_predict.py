#!/usr/bin/env python3

"""Train on training data. This will open up a file in ../trainingdata/ and get
the sweet, sweet instances out of it. And then train on them and produce a
maxent classifier for a given target language and source word."""

import nltk
import pickle
import sys
import argparse
from operator import itemgetter

from nltk.classify.maxent import MaxentClassifier

import util_run_experiment
from wsd_problem import WSDProblem
from parse_corpus import extract_wsd_problems
import read_gold
import features
import stanford
from co_occur import Occurrence
import train_from_extracted


def get_four_friends(target):
    all_languages = set(['es','fr','nl','de','it'])
    four_friends = all_languages - set([target])
    print(four_friends)
    return four_friends 

def extend_features(features,more_features,frd1,frd2,frd3,frd4):
    features["friend_{}({})".format(frd1,more_features[0])] = True
    features["friend_{}({})".format(frd2,more_features[1])] = True
    features["friend_{}({})".format(frd3,more_features[2])] = True
    features["friend_{}({})".format(frd4,more_features[3])] = True

    return features

def get_training_data_from_extracted(sourceword, targetlang):
    """Return a list of (featureset, label) for training."""


    frd1,frd2,frd3,frd4 = sorted(list(get_four_friends(targetlang)))  ##Get other four languages.
    classfrd1,classfrd2,classfrd3,classfrd4 = get_level1_classifiers(frd1,frd2,frd3,frd4,sourceword)

    ##Get the intersection of four training sentences.
    tool_class = Occurrence(sourceword,frd1,frd2)

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

    print("the length of them...",len(contexts),len(indices),len(labelss))
    #input()
    answers = []
    for context, index, labels in zip(contexts, indices, labelss):
        problem = WSDProblem(sourceword, context,
                             testset=False, head_index=index)

            #print(more_featuress)
        for label in labels:
            if label == '': continue
            problems.append(problem)
            #more_features = intersection[context]
            answers.append(label)

    for problem,answer in zip(problems, answers):
        level1_features = features.extract(problem)
        answer_frd1 = classfrd1.classify(level1_features)
        answer_frd2 = classfrd2.classify(level1_features)
        answer_frd3 = classfrd3.classify(level1_features)
        answer_frd4 = classfrd4.classify(level1_features)
        level2_features = extend_features(level1_features,(answer_frd1,answer_frd2,answer_frd3,answer_frd4),frd1,frd2,frd3,frd4)
        label = answer
        assert(type(label) is str)
        #print("=================@@@@features {}\n@@@@label{}\n".format(featureset,label))
        out.append((level2_features, label))
    print("###Length of the output should be the same{}\n".format(len(out)))
    return out

def get_maxent_classifier(sourceword, target):
    instances = get_training_data_from_extracted(sourceword, target)
    instances = train_from_extracted.remove_onecount_instances(instances)
    print("got {0} training instances!!".format(len(instances)))
    print("... training ...")
    classifier = MaxentClassifier.train(instances,
                                        trace=0,
                                        max_iter=20,
                                        algorithm='megam')
    print("LABELS", classifier.labels())
    return classifier

def get_level1_answers(classifier_frd1,classifier_frd2,classifier_frd3,classifier_frd4,featureset):
    frd1,frd2,frd3,frd4 = sorted(list(get_four_friends(target)))
    answer_frd1 = classifier.classify()

def get_level1_classifiers(frd1,frd2,frd3,frd4,sourceword):
    
    classifier_frd1 = util_run_experiment.get_pickled_classifier(sourceword,frd1,'level1')
    classifier_frd2 = util_run_experiment.get_pickled_classifier(sourceword,frd2,'level1')
    classifier_frd3 = util_run_experiment.get_pickled_classifier(sourceword,frd3,'level1')
    classifier_frd4 = util_run_experiment.get_pickled_classifier(sourceword,frd4,'level1')

    return classifier_frd1,classifier_frd2,classifier_frd3,classifier_frd4


def train_l2_classifiers():
    all_languages = [sys.argv[1]]
    path = "../L2pickle"
    all_words = util_run_experiment.final_test_words
    nltk.classify.megam.config_megam(bin='/usr/local/bin/megam')
    
    for sourceword in all_words:
        for target in all_languages:
            level2_classifier = get_maxent_classifier(sourceword, target)
            pickle.dump( level2_classifier,open( "{}/{}.{}.level2.pickle".format(path,sourceword,target),'wb')  )
            #answer = level2_classifier.classifiy( {"cw(deposit)":True,"cw(money)":True,"cw(finacial)":True}  )
            #print("the answer::::",answer)
            ###pickle the level2 classifiers...        
            #test_level2(sourceword,target,level2_classifier)


if __name__ == "__main__": 
    stanford.taggerhome = '/home/liucan/stanford-postagger-2012-11-11'
    train_l2_classifiers()
    #test_level2('bank','es')
    #lan  sys.argv[1]
    #get_four_friends(lan)
    #get_training_data_from_extracted('bank','de')
