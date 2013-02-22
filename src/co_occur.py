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

	def __init__(self):

		languages = sys.argv[1]
		lan1,lan2 = sorted(languages.split('-'))  ##The pair by alphabetic order. 
		self.lan1 = lan1
		self.lan2 = lan2
		self.lan1_labels = []
		self.lan2_labels = []
		self.sent_pairs = []
		self.lan1FN = ""
		self.lan2FN = ""
		self.labelFN = ""
		self.cooccur = defaultdict(  lambda: defaultdict (lambda:0))
		

	def get_labels(self):

		fileIN = open(self.labelFN,'r')
		self.lan1_labels = []  ## TO
		self.lan2_labels = []  ### TO
		fileIN.close()

	def get_aligned(self):
		self.sent_pairs = [] ### TO


	def get_count(self):
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




















				
