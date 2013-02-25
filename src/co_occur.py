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
		self.lan1_labels = self.get_labels(sourceword,lan1)
		self.lan2_labels = self.get_labels(sourceword,lan2)       		

	def get_labels(self,sourceword,lan):
		path = "../Senses/"
		labels = {}
		lanFN = path+sourceword +"." + lan 		
		fileO = open(lanFN,'r')
		line = fileO.readline()
		while line:
			labels[line.strip()] = 1
			line = fileO.readline()
		
		fileO.close()
		return labels
	

	def get_aligned(self,sourceword,lan1,lan2):
                
		self.sent_pairs = [] ### TO

	def get_common_sents(self,sourceword,lan1,lan2):
		#path = "../trainingdata/"
		path ="../"
		lan1FN = path+sourceword +"."+ lan1 + ".train"
		lan2FN = path+sourceword +"."+ lan2 + ".train"
		
		IN1 = open(lan1FN,'r')
		IN2 = open(lan2FN,'r')
		
		line1 = IN1.readline()
		line2 = IN2.readline()
		dic1 = defaultdict(lambda:0)
		dic2 = defaultdict(lambda:0)
		count = 1
		triple = []
		mappings1 = {}
		mappings2 = {}
		while line1:
			
			triple.append(line1.strip())
			if count %3 ==1:  ##add this sentence to 
				dic1[line1.strip()] +=1
			if count%3==0:
				mappings1[triple[0]] = (triple[2])
				triple = []
			count+=1
			line1 = IN1.readline()

		count = 1
		triple = []
		while line2:
			
			triple.append(line2.strip())
			if count %3 ==1:  ##add this sentence to s
				dic2[line2.strip()] +=1
			if count%3==0:	
				mappings2[triple[0]] = (triple[2])
				triple = []
			count +=1
			line2 = IN2.readline()
		
		##Finding the intersection of the two dictionaries.
		total = 0
		count = 0
		sent_pairs = []
		for key in dic1:
			if key in dic2:
				#print("\nOverlap:::",dic1[key],dic2[key],"\n",key)
				pair = (mappings1[key],mappings2[key])
				sent_pairs.append(pair)
				total += dic2[key]
				count +=1
		print("Total overlapped sents:",total,count)
		return sent_pairs


	def get_count(self,sent_pairs):
		print("Counting from....:",len(sent_pairs))
		temp_dict = defaultdict(lambda:  defaultdict(lambda:0))
		ll = sent_pairs
		print('ll',ll)
		for lan1_w,lan2_w in ll:
			print(lan1_w,lan2_w)
			temp_dict[lan1_w][lan2_w] +=1
		
		self.cooccur = temp_dict
		print(temp_dict)

		
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
		templist = []#defaultdict(  lambda: defaultdict(lambda:0))
		tempdict = {}
		for lan1_label in self.lan1_labels:
			for lan2_label in self.lan2_labels:
				templist.append((lan1_label,lan2_label,self.cooccur[lan1_label][lan2_label]))
		for l1,l2,count in tempdict:	
			tempdict[(l1,l2)] = count

		return tempdict
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
	dd = cls.get_distribution()
	occur = dd#cls.cooccur
	#print(occur)
	for key in occur:
		print(key,occur[key])
		#for w2 in occur:
		#	print(key,w2,occur[key][w2])

















				
