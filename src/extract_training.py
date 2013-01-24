#!/usr/bin/env python3

"""Given a source word, source text and target text filenames, produce training
data files."""

import sys
import argparse
import functools

from nltk.stem import wordnet
wnl = wordnet.WordNetLemmatizer()

## Given a pair of lines (src,trg) we need to decide whether this is a source
## line we're interested in, and then we need to decide what the target word
## sense is.

@functools.lru_cache
def get_tagger()
    ## these need to be environment variables or commandline arguments.
    tagger = '/path/to/wsj-0-18-bidirectional-distsim.tagger'
    jar = '/path/to/stanford-postagger.jar'
    stanford_tagger = StanfordTagger(tagger, jar)
    return stanford_tagger

def keep_source_sentence(sentence, sourceword):
    tokenized = nltk.word_tokenize(sentence)
    tagger = get_tagger()
    tagged_sentence = tagger.tag(tokenized)

    ## now check whether we have the source word as a noun...

    ## now find the target-language sense...

    return False

def main():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, nargs=1, required=True)
    parser.add_argument('--sourcetext', type=str, nargs=1, required=True)
    parser.add_argument('--targettext', type=str, nargs=1, required=True)
    args = parser.parse_args()

    sourcefn = args.sourcetext[0]
    targetfn = args.targettext[0]
    sourceword = args.sourceword[0]

    with open(sourcefn) as infile_s, open(targetfn) as infile_t:
        for source, target in zip(infile_s, infile_t):
            source = source.strip()
            target = target.strip()

            print("source:", source)
            print("target:", target)

if __name__ == "__main__": main()
