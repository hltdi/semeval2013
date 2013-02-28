#!/usr/bin/env python3

"""Just making sure we know how to do classifiers in NLTK..."""

from __future__ import print_function

import nltk

from nltk.classify.decisiontree import DecisionTreeClassifier
from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.classify.maxent import MaxentClassifier

# Define a feature detector function.
def document_features(document):
    return dict([('contains-word(%s)' % w, True) for w in document])

documents = [
    ("food jam apples bananas bagels peanut butter", "food"),
    ("butter steak beef", "food"),
    ("butter steak beef", "food"),
    ("hat trick space jam basketball play", "sports"),
    ("hat trick basketball hockey", "sports"),
    ("play sports espn", "sports")
]

def main():
    nltk.classify.megam.config_megam(bin='/usr/local/bin/megam')
    instances = []
    for (text, label) in documents:
        feats = document_features(text.split())
        instances.append( (feats, label) )

    feats = document_features("ham butter beef".split())
    for klass in [NaiveBayesClassifier,
                  MaxentClassifier,
                  DecisionTreeClassifier]:
        print("trying", klass)

        if klass is MaxentClassifier:
            classifier = klass.train(instances, algorithm='megam')
        else:
            classifier = klass.train(instances)
        print(classifier.labels())
        try:
            dist = classifier.prob_classify(feats)
            for key in dist.samples():
                print(" ", key, dist.prob(key))
        except:
            print("no prob_classify, that's fine.")
        print(classifier.classify(feats))

if __name__ == "__main__": main()
