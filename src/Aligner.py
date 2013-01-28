"""
The aligner.
Given: a pair of sentences of interest. Plus their alignment.
Output: The aligned sentence.
"""


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


if __name__ =="__main__":
    a = Aligner("")
    a.align_pair("speech FROM THE THRONE".split(),"SS FF TT PP".split(),"0-1 2-0 1-3 3-2".split())
