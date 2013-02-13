#!/usr/bin/env python3

"""Do the preprocessing that we need before running the aligner.

Currently, just does sentence-level and word-level tokenization, then prints all
the tokens separated by spaces."""

import argparse
import nltk

def main():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--infile', type=str, nargs=1, required=True)
    parser.add_argument('--outfile', type=str, nargs=1, required=True)
    args = parser.parse_args()

    infn = args.infile[0]
    outfn = args.outfile[0]

    with open(infn) as infile, open(outfn, "w") as outfile:
        for line in infile:
            sents = nltk.sent_tokenize(line)
            tokens = []
            for sent in sents:
                tokens += nltk.word_tokenize(sent)
            print(" ".join(tokens), file=outfile)

if __name__ == "__main__": main()
