"""
This file gets the co-occurrence table for languages.
1. Just count
2. A distribution from the count
3. co-occurrence distri and classifier output on the same scale.
"""
import sys
from collections import defaultdict
### import the alignment file.


class Occurrence:

	def __init__(self,sourceword,lan1,lan2):

 
		#lan1,lan2 = sorted(languages.split('-'))  ##The pair by alphabetic order. 
		self.sent_pairs = []
		self.cooccur = defaultdict(  lambda: defaultdict (lambda:0))
		#self.lan1_labels = self.get_labels(sourceword,lan1)
		#self.lan2_labels = self.get_labels(sourceword,lan2)       		

	def get_labels(self,sourceword,lan):
		path = "../Senses/"
		labels = {}
		lanFN = path+sourceword +"." + lan 		
		fileO = open(lanFN,'r')
		line = fileO.readline()
		while line:
			labels[line.strip()] = 1
			line = file0.readline()
		
		fileO.close()
		return labels
	

	def get_aligned(self,sourceword,lan1,lan2):
                
		self.sent_pairs = [] ### TO

	def get_common_sents(self,sourceword,lan1,lan2):
		path = "../trainingdata/"
		lan1FN = path+sourceword +"."+ lan1 + ".train"
		lan2FN = path+sourceword +"."+ lan2 + ".train"
		
		IN1 = open(lan1FN,'r')
		IN2 = open(lan2FN,'r')
		
		line1 = IN1.readline()
		line2 = IN2.readline()
		origin_lan1 = []
		origin_lan2 = []
		words_lan1 = []
		words_lan2 = []
		sentences_lan1 = set()
		sentences_lan2 = set()
		count = 1
		triple = []
		while line1:
			
			triple.append(line1.strip())

			if count %3 ==1:  ##add this sentence to set.
				sentences_lan1.add(line1.strip())
			if count%3==0:
				origin_lan1.append(triple)
				triple = []
			count+=1
			line1 = IN1.readline()

		count = 1
		triple = []
		while line2:
			
			triple.append(line2.strip())
			if count %3 ==1:  ##add this sentence to set.
				sentences_lan2.add(line2.strip())
			if count%3==0:	
				origin_lan2.append(triple)
				triple = []
			count +=1
			line2 = IN2.readline()

		intersection = sentences_lan1 & sentences_lan2

		##Now only get the ones on in the intersection
		for triple in origin_lan1:
			if triple[0] in intersection:
				words_lan1.append(triple[2])
		for triple in origin_lan2:
                        if triple[0] in intersection:
                                words_lan2.append(triple[2])
		
		sent_pairs = zip(words_lan1,words_lan2)
		print(origin_lan1[:1])
		print(origin_lan2[:1])
		print(list(intersection)[:1])
		print(words_lan1[:5])
		print(words_lan2[:5])
		print(list(self.sent_pairs)[:5])
		#print(sentences_lan1[:5])
		return sent_pairs
	def get_count(self,sent_pairs):
		print(len(list(sent_pairs)))
		temp_dict = defaultdict(lambda:  defaultdict(lambda:0))
		for lan1_w,lan2_w in list(sent_pairs):
			#print(lan1_w,lan2_w)
			temp_dict[lan1_w][lan2_w] +=1
		

		#print(temp_dict)
		"""
		for lan1,lan2 in self.sent_pairs:
			presence1 = []
			presence2 = []
			for word in lan1:
				if word in self.lan1_labels:  presence1.append(word)
			for word in lan2:
				if word in self.lan2_labels:  presence2.append(word)		

			for lan1_word in presence1:
				for lan2_word in presence2:
					self.cooccur[lan1_word][lan2_word] +=1
		"""

	def get_distribution(self):
		"""Change the counts into a distribution."""
		pass
		self.cooccur = self.cooccur

	def write_data(self):
		fileOUT = open("",'w') ### TO
		for lan1_word in self.cooccur:
			for key, value in self.cooccur[lan1_word]:
				fileOUT.write(key+","+value+"\n")
		fileOUT.close()


if __name__ == "__main__":  
	cls = Occurrence('bank','de','it')
	sents = cls.get_common_sents('bank','de','it')
	cls.get_count(sents)
	occur = cls.cooccur
	#print(occur)
	#for key in occur:
#		for w2 in occur:
#			print(key,w2,occur[key][w2])

















				
