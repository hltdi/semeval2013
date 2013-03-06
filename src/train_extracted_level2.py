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

from wsd_problem import WSDProblem
from parse_corpus import extract_wsd_problems
import read_gold
import features
import stanford
from co_occur import Occurrence

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
    ##Get the intersection of four training sentences.
    tool_class = Occurrence(sourceword,frd1,frd2)
    intersection = tool_class.get_common_four_sents(sourceword,frd1,frd2,frd3,frd4)

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
    extention = []
    for context, index, labels in zip(contexts, indices, labelss):
        #print(index)
        if context in intersection:  ##If this sentence also appears in 4 other languages, we can use more features...
            problem = WSDProblem(sourceword, context,
                             testset=False, head_index=index)
            for label in labels:
                if label == '': continue
                problems.append(problem)
                more_features = intersection[context]
                extention.append(more_features)
                answers.append(label)
    print("###intersection for five languages....{}\n".format(len(extention)))

    for problem,answer,more_feature in zip(problems, answers,extention):
        featureset = features.extract(problem)
        featureset = extend_features(featureset,more_feature,frd1,frd2,frd3,frd4)
        label = answer
        assert(type(label) is str)
        print("=================@@@@features {}\n@@@@label{}\n".format(featureset,label))
        out.append((featureset, label))
    print("###Length of the output should be the same{}\n".format(len(out)))
    return out

def get_maxent_classifier(sourceword, target):
    instances = get_training_data_from_extracted(sourceword, target)
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
    path = "../L1pickle/"
    pickle_frd1  = sourceword +"."+frd1 + ".level1.pickle"
    pickle_frd2  = sourceword +"."+frd2 + ".level1.pickle"
    pickle_frd3  = sourceword +"."+frd3 + ".level1.pickle"
    pickle_frd4  = sourceword +"."+frd4 + ".level1.pickle" 

    classifier_frd1 = pickle.load(open(path+pickle_frd1,'rb'))
    classifier_frd2 = pickle.load(open(path+pickle_frd2,'rb'))
    classifier_frd3 = pickle.load(open(path+pickle_frd3,'rb'))
    classifier_frd4 = pickle.load(open(path+pickle_frd4,'rb'))

    return classifier_frd1,classifier_frd2,classifier_frd3,classifier_frd4


def train_l2_classifiers():
    path = "../L2pickle"
    all_target_languages = "nl de es fr it".split()
    all_words = "bank coach education execution figure job letter match mission mood movement occupation paper passage plant post pot range rest ring scene side soil strain test".split()
    all_languages = ['es']
    all_words = ['bank']
    nltk.classify.megam.config_megam(bin='/usr/local/bin/megam')
    for sourceword in all_words:
        for target in all_languages:
            level2_classifier = get_maxent_classifier(sourceword, target)
            pickle.dump( level2_classifier,open( "{}/{}.{}.level2.pickle".format(path,sourceword,target),'wb')  )
            #answer = level2_classifier.classifiy( {"cw(deposit)":True,"cw(money)":True,"cw(finacial)":True}  )
            #print("the answer::::",answer)
            ###pickle the level2 classifiers...        
            test_level2(sourceword,target,level2_classifier)


                        
def test_level2(sourceword,target,level2_classifier):
    path = "../L2pickle"
    #level2_classifier = pickle.load( open("{}/{}.{}.level2.pickle".format(path,sourceword,target,'rb')) )
    level2_classifier = pickle.load( 
                           open( "{}/{}.{}.level2.pickle".format(path,sourceword,target)  ,'rb') 
                                      )
    frd1,frd2,frd3,frd4 = sorted(list(get_four_friends(target)))   ##Need 4 more features from level1.
    classfrd1,classfrd2,classfrd3,classfrd4 = get_level1_classifiers(frd1,frd2,frd3,frd4,sourceword)

    fn = "../trialdata/alltrials/{0}.data".format(sourceword)
    problems = extract_wsd_problems(fn)
    gold_answers = read_gold.get_gold_answers(sourceword, target)
    for problem in problems:
        level1_features = features.extract(problem)
        answer_frd1 = classfrd1.classify(level1_features)
        answer_frd2 = classfrd2.classify(level1_features)
        answer_frd3 = classfrd3.classify(level1_features)
        answer_frd4 = classfrd4.classify(level1_features)
        level2_features = extend_features(level1_features,(answer_frd1,answer_frd2,answer_frd3,answer_frd4),frd1,frd2,frd3,frd4)
        level2_answer = level2_classifier.classify(level2_features)
        print(level2_answer)
        label = gold_answers[problem.instance_id]
        print("CORRECT" if label == level2_answer else "WRONG", end=" ")
        print("should be:", label)
    



if __name__ == "__main__": 
    stanford.taggerhome = '/home/liucan/stanford-postagger-2012-11-11'
    train_l2_classifiers()
    #test_level2('bank','es')
    #lan  sys.argv[1]
    #get_four_friends(lan)
    #get_training_data_from_extracted('bank','de')
