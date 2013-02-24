#!/usr/bin/env python3

import nltk
from nltk.stem import wordnet
wnl = wordnet.WordNetLemmatizer()

START = "QQQSTARTHEADQQQ"
END = "QQQENDHEADQQQ"

class WSDProblem:
    """Class where we'll stash all the information about a given WSD problem."""

    ## TODO(alexr): this needs to be reworked so we can sensibly build them from
    ## training data...
    ## Probably we'll pass a flag to say whether we're building from the test
    ## set or the training set. If it's the training set, we'll pass an index
    ## for the head word, and otherwise, the constructor will look for the head
    ## tags. Passing 'count' is probably not a good idea.
    def __init__(self, source_lex, count, context, instance_id):
        """Given the source lexical item (ie, uninflected version of the source
        word) and the context, build a WSD problem that we can solve later."""
        self.source_lex = source_lex
        self.context = context
        self.head_count = count
        self.instance_id = instance_id
        self.head_indices = []

        context = context.replace("<head>", START)
        context = context.replace("</head>", END)

        sentences = nltk.sent_tokenize(context)
        tokenized = [nltk.word_tokenize(sent) for sent in sentences]
        for sent_index,sent in enumerate(tokenized):
            for word_index,word in enumerate(sent):
                if word.startswith(START):
                    assert word.endswith(END)
                    sent[word_index] = word.replace(START,"").replace(END,"")
                    self.head_indices.append((sent_index,word_index))

        self.tokenized = tokenized
        self.lemmatized = [[wnl.lemmatize(token.lower()) for token in sent]
                           for sent in self.tokenized]

    def __str__(self):
        return "<<{0}: {1}>>".format(self.source_lex, self.context)
