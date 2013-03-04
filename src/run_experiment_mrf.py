#!/usr/bin/env python3

import itertools
import math
import random

from loopybp import Edge
from loopybp import Node
from loopybp import beliefprop
from loopybp import possible_values

def main():
    langs = "de es fr it nl".split()

    for lang in langs:
        unary = {}
        for i in range(10):
            val = lang + str(i)
            penalty = random.randint(1, 100)
            unary[val] = penalty
        langnode = Node(lang, unary)

    ## get all the combinations of nodes.
    langpairs = list(itertools.combinations(langs, 2))

    ## create an edge for each language pair.
    for l1, l2 in langpairs:
        edgepotentials = {}
        for val1 in possible_values(l1):
            for val2 in possible_values(l2):
                edgepotentials[(val1,val2)] = random.randint(1, 100)
        Edge(l1, l2, edgepotentials)

    best_values = beliefprop(100)
    print(best_values)

if __name__ == "__main__": main()
