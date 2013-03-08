#!/usr/bin/env python3

"""Extract all of the target-language senses from the gold standard files in the
evaluation data. We'll go with this until we get good aligners and stemmers for
the Europarl intersection...
"""

import sys
import argparse
from operator import itemgetter

def senses(sourceword, target):
    """Given a source word and a target language, load up the gold answers for
    that word and return a set of the target-language translations (sense
    labels) for that source word."""
    out = set()
    fn = "../eval/{0}.gold.{1}".format(sourceword, target)
    with open(fn) as infile:
        for line in infile:
            splitted = line.split(None, 3)
            problemid = splitted[1]
            rest = splitted[3].strip()
            assert rest.endswith(';')
            rest = rest[:-1]

            word_count_pairs = []
            for wordandcount in rest.split(';'):
                word, count = wordandcount.rsplit(None, 1) # count is rightmost
                word = word.lower()
                out.add(word)
    return out

def main():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, nargs=1, required=True)
    parser.add_argument('--targetlang', type=str, nargs=1, required=True)
    args = parser.parse_args()

    all_target_languages = "de es fr it nl".split()
    assert args.targetlang[0] in all_target_languages
    target = args.targetlang[0]
    sourceword = args.sourceword[0]

    labels = senses(sourceword, target)
    print("possible labels...")
    for label in labels:
        print(" ", label)

def generate_all():
    path = "../Senses/"
    all_target_languages = "de es fr it nl".split()
    all_words = []
    for target in all_target_languages:
        for sourceword in all_words:
            fileOUT = open(path + sourceword +"."+sourceword,'w')
            labels = senses(sourceword, target)
            for label in labels:
                fileOUT.write(label + "\n")
            fileOUT.close()

if __name__ == "__main__": generate_all()#main()
