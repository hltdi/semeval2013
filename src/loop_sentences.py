#!/usr/bin/env python3

"""
At first, let's just extract and loop over the sentences in all the *.data files
that are specified on the command line.
"""

import sys
from xml.sax import handler, make_parser

class SentenceExtractor(handler.ContentHandler):
    def __init__(self):
        self.sentences = []
        self.sentence_id = None
        self.cur_sentence = ""
        self.in_context = False

    def characters(self, content):
        # print("characters", content)
        if self.in_context:
            self.cur_sentence += content

    def startElement(self, name, attrs):
        if name == "lexelt":
            lexelt = attrs.get("item")
            print("LEXELT", lexelt)

        if name == "instance":
            self.sentence_id = attrs.get("id")
            self.cur_sentence = ""

        if name == "context":
            self.in_context = True

        if name == "head":
            self.cur_sentence += "<head>"

    def endElement(self, name):
        if name == "context":
            self.in_context = False
            self.sentences.append(self.cur_sentence)

        if name == "head":
            self.cur_sentence += "</head>"

def extract(fn):
    handler = SentenceExtractor()
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.parse(fn)

    for sentence in handler.sentences:
        print("***")
        print(sentence)

def main():
    fns = sys.argv[1:]
    print("input files:", fns)
    for fn in fns:
        extract(fn)

if __name__ == "__main__": main()
