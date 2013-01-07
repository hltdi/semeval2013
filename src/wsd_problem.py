#!/usr/bin/env python3

class WSDProblem:
    """Class where we'll stash all the information about a given WSD problem."""

    def __init__(self, source_lex, context):
        """Given the source lexical item (ie, uninflected version of the source
        word) and the context, build a WSD problem that we can solve later."""
        self.source_lex = source_lex
        self.context = context
        self.features = None

    def extract_features(self):
        """Extract features from the context."""
        self.features = set()

    def solve_one_best(self, target=None, solver=None):
        """Return the one best translation in the specified target language.
        Default to using a maxent classifier."""
        return "orilla"

    def solve_one_best(self, target=None, solver=None):
        """Return a list of the best translations in the specified target
        language. Default to using a maxent classifier."""
        return "orilla banco".split()

def main():
    pass

if __name__ == "__main__": main()
