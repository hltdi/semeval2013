"""Given an English sentence read from the paralell corpus, determine whether it has the word
we're interested in"""

import nltk
from nltk.corpus import brown
from nltk.stem.porter import PorterStemmer

class FindSent:
    
    def __init__(self):
        self.targets = ['bank','movement','occupation','passage','plant']
        self.nouns = ['NN','NNS','NNP']
    def bigram_pos(self,sentence):  ##Not sure which is good
        """Use bigram tagger to tag the sentence.Return a list"""
        brown_tagged_sents = brown.tagged_sents(categories='news')
        bigram_tagger = nltk.BigramTagger(brown_tagged_sents)
        tokenized = nltk.word_tokenize(sentence)
        #tagged_sentence = bigram_tagger.tag(tokenized)
        tagged_sentence = nltk.pos_tag(tokenized)
        return tagged_sentence

    def porter_stemmer(self,tagged_sentence):  ##Not sure which is good
        """returns (word, stem,POS)"""
        stemmer = PorterStemmer()
        words = [x[0] for x in tagged_sentence]
        pos_tags = [x[1] for x in tagged_sentence]
        stems = [stemmer.stem(x) for x in words]
        word_stem_pos = zip(words,stems,pos_tags)
        return word_stem_pos

    def find_sent(word_stem_pos):
        """if it's the sentence we're interested in, return target word.
        Otherwise return NONE"""
        targets_found = []   ##What to do if there're multiple.
        for word,stem,pos in word_stem_pos:
            if stem in self.targets and pos in nouns:
                targets_found.append([word,stem,pos])
        return targets_found
                
        
##POS tag a sentence.
##Use bigram tagger from brown corpos. ??or others.


if __name__ == "__main__":
    c = FindSent()
    sentence = c.bigram_pos('I went to the banks')
    result = c.porter_stemmer(sentence)
    print(result)
