#!/usr/bin/env python3

"""Just making sure we know how to do classifiers in NLTK..."""

import nltk

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

instances = []

for (text, label) in documents:
    feats = document_features(text.split())
    instances.append( (feats, label) )

classifier = nltk.classify.naivebayes.NaiveBayesClassifier.train(instances)
print(classifier.labels())
feats = document_features("ham butter beef".split())
dist = classifier.prob_classify(feats)
for key in dist.samples():
    print(" ", key, dist.prob(key))
print(classifier.classify(feats))
