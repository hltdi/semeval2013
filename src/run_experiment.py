#!/usr/bin/env python3

import sys
import argparse

from parse_corpus import extract_wsd_problems

def solve_one_best(problem, target, solver=None):
    """Return the one best translation in the specified target language.
    Default to using a maxent classifier."""

    return "banco"

def solve_oof(problem, target, solver=None):
    """Return a list of the best translations in the specified target
    language. Default to using a maxent classifier."""
    return "orilla banco".split()


def output_one_best(problem, target, solution):
    """Return output for a solution for the one-best."""
    return "{0}.{1} {2} :: {3};".format(problem.source_lex,
                                        target,
                                        problem.instance_id,
                                        solution)

def main():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, nargs=1, required=True)
    parser.add_argument('--targetlang', type=str, nargs=1, required=True)
    parser.add_argument('--classifier', type=str, nargs=1, required=False)
    args = parser.parse_args()

    all_target_languages = "de es fr it nl".split()
    if args.targetlang:
        assert args.targetlang[0] in all_target_languages
        targets = args.targetlang
    sourceword = args.sourceword[0]

    fns = ["../trialdata/alltrials/{0}.data".format(sourceword)]

    with open("../eval/{0}.output".format(sourceword), "w") as outfile:
        for fn in fns:
            for target in targets:
                problems = extract_wsd_problems(fn)
                for problem in problems:
                    answer = solve_one_best(problem, target)
                    print(output_one_best(problem, target, answer),
                          file=outfile)

if __name__ == "__main__": main()
