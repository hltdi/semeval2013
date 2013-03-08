#!/usr/bin/env python3

import nltk
from nltk.stem import wordnet
wnl = wordnet.WordNetLemmatizer()

import stanford

START = "QQQSTARTHEADQQQ"
END = "QQQENDHEADQQQ"

class WSDProblem:
    """Class where we'll stash all the information about a given WSD problem."""

    ## TODO(alexr): this needs to be reworked so we can sensibly build them from
    ## training data...
    ## Probably we'll pass a flag to say whether we're building from the test
    ## set or the training set. If it's the training set, we'll pass an index
    ## for the head word, and otherwise, the constructor will look for the head
    ## tags.
    ## TODO(alexr): let's flatten out the representation. Let's just store a
    ## one-level list, then indices make more sense.
    def __init__(self, source_lex, context,
                 testset=False, instance_id=None, head_index=None):
        """Given the source lexical item (ie, uninflected version of the source
        word) and the context, build a WSD problem that we can solve later."""
        self.source_lex = source_lex
        self.instance_id = instance_id

        if testset:
            self.init_testset(context)
        else:
            self.init_trainingset(context, head_index)

        self.lemmatized = [wnl.lemmatize(token.lower())
                           for token in self.tokenized]

    def init_testset(self, context):
        """If we're coming from the test set, we haven't tagged yet. Probably
        tag now. Also we're probably not tokenized."""
        assert type(context) is str
        self.head_indices = []

        context = context.replace("<head>", START)
        ## XXX(alexr): this is completely terrible.
        context = context.replace("</head>", END + " ")

        sentences = nltk.sent_tokenize(context)
        tokenized = [nltk.word_tokenize(sent) for sent in sentences]

        index = 0
        for sent_index,sent in enumerate(tokenized):
            for word_index,word in enumerate(sent):
                if word.startswith(START):
                    if not word.endswith(END):
                        print(repr(word))
                        print(tokenized)
                        print(context)
                        assert False
                    sent[word_index] = word.replace(START,"").replace(END,"")
                    self.head_indices.append(index)
                index += 1
        self.tokenized = []
        for sent in tokenized:
            self.tokenized += sent

    def init_trainingset(self, context, head_index):
        """In this case, we should get context as a tagged string, out of the
        training data files. Also a particular head_index. We still need to
        lemmatize."""
        assert type(context) is str
        assert type(head_index) is int
        split = context.split()
        self.tagged = [nltk.tag.str2tuple(tok) for tok in split]
        self.tokenized = nltk.tag.untag(self.tagged)
        self.head_indices = [head_index]

    def __str__(self):
        return "<<{0}: {1}>>".format(self.source_lex, self.tagged)
