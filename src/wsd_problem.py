#!/usr/bin/env python3

class WSDProblem:
    """Class where we'll stash all the information about a given WSD problem."""

    def __init__(self, source_lex, count, context, instance_id):
        """Given the source lexical item (ie, uninflected version of the source
        word) and the context, build a WSD problem that we can solve later."""
        self.source_lex = source_lex
        self.context = context
        self.head_count = count
        self.instance_id = instance_id
        self.features = None

    def extract_features(self):
        """Extract features from the context."""
        self.features = set()

    def __str__(self):
        return "<<{0}: {1}>>".format(self.source_lex, self.context)
