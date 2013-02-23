"""
The aligner.
Given: a pair of sentences of interest. Plus their alignment.
Output: The aligned sentence.
"""

from collections import defaultdict
from operator import itemgetter

class Aligner:

    def __init__(self,targetFile):
        self.enFile = ""
        self.targetFile = ""
        self.alignFile = ""

    def align_pair(self,english,target,align):
        """The input must be tokenized..."""
        aligned_sentence = []
        align_dict = {}
        for pair in align:
            en,tar = pair.split('-')
            align_dict[int(en)] = int(tar)
        for i in range(len(english)):
            aligned_sentence.append((english[i],target[align_dict[i]]))
        print(aligned_sentence)
        return aligned_sentence

    def align_all(self):  ###not useful... need tokenized sentence.
        sentence_triples = []
        enIN = open(self.enFile,'r')
        targetIN = open(self.targetFile,'r')
        alignIN = open(self.alignFile,'r')

        en_line = enIN.readline()
        targetIN = targetIN.readline()
        alignIN = alignIN.readline()
        while en_line:
            en_line = enIN.readline()
            targetIN = targetIN.readline()
            alignIN = alignIN.readline()

def target_words_for_each_source_word(ss, ts, alignment):
    """Given a list of tokens in source language, a list of tokens in target
    language, and a list of Berkeley-style alignments of the form target-source,
    for each source word, return the list of corresponding target words."""
    alignment = [tuple(map(int, pair.split('-'))) for pair in alignment]
    out = [list() for i in range(len(ss))]
    alignment.sort(key=itemgetter(1))
    for (ti,si) in alignment:
        out[si].append(ts[ti])
    return out

def sort_alignment(alignment):
    """Take a string, return a string."""
    alignment = alignment.split()
    alignment = [tuple(map(int, pair.split('-'))) for pair in alignment]
    alignment.sort(key=itemgetter(1))
    return " ".join(["{0}-{1}".format(tup[0],tup[1]) for tup in alignment])

if __name__ =="__main__":
    a = Aligner("")
    a.align_pair("speech FROM THE THRONE".split(),
                 "SS FF TT PP".split(),
                 "0-1 2-0 1-3 3-2".split())
    en = "madam president , on a point of order .".split()
    de = "frau präsidentin , zur geschäftsordung .".split()
    import random
    alignment = "0-0 5-8 4-7 3-6 3-3 2-2 1-1".split()
    random.shuffle(alignment)
    print(target_words_for_each_source_word(en, de, alignment))
