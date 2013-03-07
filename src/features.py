#!/usr/bin/env python3

import sys
import argparse

import nltk

from parse_corpus import extract_wsd_problems
import stanford

DEBUG=False

## make a bunch of functions from problems to features.
def bagofwords(problem):
    """Bag of words features."""
    tokenized = nltk.tag.untag(problem.tagged)
    return dict([('cw(%s)' % w, True) for w in tokenized])

def bagoflemmas(problem):
    """Bag of lemma features."""
    ## 'cl' for 'contains lemma'. bag of lemma features
    return dict([('cl(%s)' % w, True) for w in problem.lemmatized])

def wordform_and_tag_and_lemma(problem):
    """Literal form, tag, and lemma of the head word."""
    out = {}
    for index in problem.head_indices:
        wordform,wordtag = problem.tagged[index]
        wordlemma = problem.lemmatized[index]
        features = {
            ('wordform(%s)' % wordform): True,
            ('wordtag(%s)' % wordtag): True,
            ('wordlemma(%s)' % wordlemma): True,
        }
        out.update(features)
    return out

WIDTH=3
def window(problem):
    """Immediate surrounding context features."""
    tokenized = nltk.tag.untag(problem.tagged)
    out = {}
    for index in problem.head_indices:
        ## window of WIDTH before
        lowerbound = max(0, index-WIDTH)
        windowfeatures = dict([('w(%s)' % w, True)
                              for w in tokenized[lowerbound:index]])
        out.update(windowfeatures)
        ## and WIDTH after
        upperbound = index+WIDTH
        windowfeatures = dict([('w(%s)' % w, True)
                              for w in tokenized[index+1:upperbound+1]])
        out.update(windowfeatures)
    return out

def window_lemmas(problem):
    """Immediate surrounding context lemmas."""
    out = {}
    for index in problem.head_indices:
        ## window of WIDTH before
        lowerbound = max(0, index-WIDTH)
        windowfeatures = dict([('wl(%s)' % w, True)
                              for w in problem.lemmatized[lowerbound:index]])
        out.update(windowfeatures)
        ## and WIDTH after
        upperbound = index+WIDTH
        windowfeatures = \
            dict([('wl(%s)' % w, True)
                  for w in problem.lemmatized[index+1:upperbound+1]])
        out.update(windowfeatures)
    return out

def window_justtags(problem):
    """Immediate surrounding tags."""
    tags = [tag for (word,tag) in problem.tagged]
    out = {}
    for index in problem.head_indices:
        ## window of WIDTH before
        lowerbound = max(0, index-WIDTH)
        windowfeatures = dict([('wt(%s)' % w, True)
                              for w in tags[lowerbound:index]])
        out.update(windowfeatures)
        ## and WIDTH after
        upperbound = index+WIDTH
        windowfeatures = dict([('wt(%s)' % w, True)
                              for w in tags[index+1:upperbound+1]])
        out.update(windowfeatures)
    return out

def window_withtags(problem):
    """Immediate surrounding tagged words."""
    tagged = [nltk.tag.tuple2str(tup) for tup in problem.tagged]
    out = {}
    for index in problem.head_indices:
        ## window of WIDTH before
        lowerbound = max(0, index-WIDTH)
        windowfeatures = dict([('wtagged(%s)' % w, True)
                              for w in tagged[lowerbound:index]])
        out.update(windowfeatures)
        ## and WIDTH after
        upperbound = index+WIDTH
        windowfeatures = dict([('wtagged(%s)' % w, True)
                              for w in tagged[index+1:upperbound+1]])
        out.update(windowfeatures)
    return out

def window_left(problem):
    """Immediate surrounding context features: just the left."""
    tokenized = nltk.tag.untag(problem.tagged)
    out = {}
    for index in problem.head_indices:
        ## window of WIDTH before
        lowerbound = max(0, index-WIDTH)
        windowfeatures = dict([('wl(%s)' % w, True)
                              for w in tokenized[lowerbound:index]])
        out.update(windowfeatures)
    return out

def window_right(problem):
    """Immediate surrounding context features: just the left."""
    tokenized = nltk.tag.untag(problem.tagged)
    out = {}
    for index in problem.head_indices:
        upperbound = index+WIDTH
        windowfeatures = dict([('wr(%s)' % w, True)
                              for w in tokenized[index+1:upperbound+1]])
        out.update(windowfeatures)
    return out

def window_bigrams(problem):
    """Get the bigrams of window size 5, realling don't know what size is good."""
    tokenized = nltk.tag.untag(problem.tagged)
    out = {}
    for index in problem.head_indices:
        upperbound = index + 5
        lowerbound = max(0,index-5)
        words_after = tokenized[index+1:upperbound+1]
        words_before = tokenized[lowerbound:index]
        print(words_before,words_after)
        bigrams_before = nltk.bigrams(words_before)
        bigrams_after = nltk.bigrams(words_after)
        bigrams_before.extend(bigrams_after)
        windowfeatures = dict( [('wbigram({}&{})'.format(w[0],w[1]), True) for w in bigrams_before]
                              )
        out.update(windowfeatures)

    print("The bigrams...",out)
    return out

def window_bigrams_with_tags(problem):
    """Get the tagged bigrams, just three before and three after"""
    tagged = [nltk.tag.tuple2str(tup) for tup in problem.tagged]
    out = {}
    for index in problem.head_indices:
        ## window of WIDTH before
        lowerbound = max(0, index-3)
        bigrams_before = nltk.bigrams(tagged[lowerbound:index])
        ## and WIDTH after
        upperbound = index+3
        bigrams_after = nltk.bigrams(tagged[index+1:upperbound+1])
        bigrams_before.extend(bigrams_after)
        windowfeatures = dict( [('wbigram({}&{})'.format(w[0],w[1]) ,True) for w in bigrams_before]  
                            )
        out.update(windowfeatures)
    return out

def extract(problem):
    """Given a WSDProblem, return the features for the sentence."""
    out = {}
    allfeatures = [
        ## bagofwords,
        ## bagoflemmas,
        wordform_and_tag_and_lemma,
        window,
        window_lemmas,
        window_justtags,
        window_withtags,
        window_left,
        window_right,
        window_bigrams,
        window_bigrams_with_tags
    ]
    for funk in allfeatures:
        extracted = funk(problem)
        if DEBUG: print(funk.__doc__.strip()); print(extracted)
        out.update(extracted)
    return out

def main():
    """Quick demo for the feature extractor."""
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, required=True)
    parser.add_argument('--taggerhome', type=str, required=True)
    args = parser.parse_args()
    sourceword = args.sourceword
    stanford.taggerhome = args.taggerhome

    fns = ["../trialdata/alltrials/{0}.data".format(sourceword)]

    for fn in fns:
        problems = extract_wsd_problems(fn)
        for problem in problems:
            print("**** PROBLEM ****")
            tokenized = nltk.tag.untag(problem.tagged)
            print(" ".join(tokenized))
            print(problem.head_indices)
            features = extract(problem)

if __name__ == "__main__": main()
