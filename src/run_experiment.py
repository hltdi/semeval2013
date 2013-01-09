#!/usr/bin/env python3

import sys

from parse_corpus import extract_wsd_problems

def solve_one_best(problem, target, solver=None):
    """Return the one best translation in the specified target language.
    Default to using a maxent classifier."""

    return "orilla"

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
    fns = sys.argv[1:]
    targets = "de es fr it nl".split()

    with open("../eval/output", "w") as outfile:
        for fn in fns:
            problems = extract_wsd_problems(fn)
            for problem in problems:
                for target in targets:
                    answer = solve_one_best(problem, target)
                    print(output_one_best(problem, target, answer),
                          file=outfile)

if __name__ == "__main__": main()
