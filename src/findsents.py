"""Given an English sentence read from the paralell corpus, determine whether it has the word
we're interested in"""

import nltk
from nltk.corpus import brown
from nltk.stem.porter import PorterStemmer
from nltk.tag.stanfordtagger import StanfordTagger
from nltk.stem import snowball


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
    def stanford_pos(self,sentence): 
        """Use the stanford POS tagger, they have many pre-trained models, we can choose. Maybe later on as an argument"""
                        
        stanford_tagger = StanfordTagger('/nfs/nfs4/home/liucan/Desktop/Final/nltk/nltk/tag/wsj-0-18-bidirectional-distsim.tagger','/nfs/nfs4/home/liucan/Desktop/Final/nltk/nltk/tag/stanford-postagger.jar')
        tokenized = nltk.word_tokenize(sentence)
        tagged_sentence = stanford_tagger.tag(tokenized)
        return tagged_sentence


    def get_snowball_stemmer(self,language):
        """The snowball stemmer that supports other languages. To use, stemmer.stem('word')"""
        if language == 'french':
            stemmer = snowball.FrenchStemmer()
        elif language == 'spanish':
            stemmer = snowball.SpanishStemmer()
        elif language == 'german':
            stemmer = snowball.GermanStemmer()
        elif language == 'dutch':
            stemmer = snowball.DutchStemmer()
        elif language == 'italian':
            stemmer = snowball.ItalianStemmer()
        else: 
            print ('Language not supported!',language)

##POS tag a sentence.
##Use bigram tagger from brown corpos. ??or others.
if __name__ == "__main__":
    c = FindSent()
    sentence = c.stanford_pos('I went to the banks')
    result = c.porter_stemmer(sentence)
    c.get_snowball_stemmer('french')
    print(result)
