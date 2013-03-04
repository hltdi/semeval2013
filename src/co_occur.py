"""
This file gets the co-occurrence table for languages.
1. Just count
2. A distribution from the count
3. co-occurrence distri and classifier output on the same scale.
"""
import math
import pickle
import sys
from collections import defaultdict
### import the alignment file.
SMOOTH = 0.2

class Occurrence:

	def __init__(self,sourceword,lan1,lan2):
		self.sent_pairs = []
		self.cooccur = defaultdict(  lambda: defaultdict (lambda:0))
		self.lan1_labels = self.get_labels(sourceword,lan1)
		self.lan2_labels = self.get_labels(sourceword,lan2)       		
		self.lan1_tags_train = set()
		self.lan2_tags_train = set()
		self.unary_counts1 = defaultdict(lambda:0)
		self.unary_counts2 = defaultdict(lambda:0)
		self.sent_pairs = []
		self.counts = {} 
		#cls = Occurrence(word,lan1,lan2)
		self.get_common_sents(word,lan1,lan2)
		self.get_count()


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
	
	def get_common_sents(self,sourceword,lan1,lan2):
		path = "../trainingdata/"
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
				self.lan1_tags_train.add(pair[0])
				self.lan2_tags_train.add(pair[1])
				self.unary_counts1[pair[0]] +=1
				self.unary_counts2[pair[1]] +=1
				#if pair[0] == '<unknown>' or pair[1] == '<unknown>': continue
				sent_pairs.append(pair)
				total += dic2[key]
				count +=1
		print("Total overlapped sents:",total,count)
		#return sent_pairs
		self.sent_pairs = sent_pairs

	def get_count(self):
		sent_pairs = self.sent_pairs
		print("Counting from....:",len(sent_pairs))
		temp_dict = defaultdict(lambda:  defaultdict(lambda:0))
		ll = sent_pairs
		#print('ll',ll)
		for lan1_w,lan2_w in ll:
			#print(lan1_w,lan2_w)
			temp_dict[lan1_w][lan2_w] +=1
		
		self.cooccur = temp_dict
		"""
		for i in temp_dict:
			#print ("===========\n")
			for key in temp_dict[i]:
				print(i,key,temp_dict[i][key])
			#print(temp_dict)
		"""
		#return temp_dict
		self.counts = temp_dict

	def get_joint(self):
		counts = self.counts
		##Extend the label set.
		SMOOTH = 0.0001
		lan1_tags = self.lan1_tags_train.union(set(self.lan1_labels.keys()))
		lan2_tags = self.lan2_tags_train.union(set(self.lan2_labels.keys()))
		total = sum( [ sum( list(counts[w1].values()  ) ) for w1 in counts ] )
		##joint probability.
		joint = {}
		check = 0
		for lan1_word in lan1_tags:
			for lan2_word in lan2_tags:
				joint_p = 1.0* (  SMOOTH + counts[lan1_word][lan2_word]  ) / (total + SMOOTH*len(lan1_tags)*len(lan2_tags))
				joint[(lan1_word +"&&"+lan2_word)] = joint_p
				joint[(lan2_word +"&&"+lan1_word)] = joint_p
				check += joint_p

		print (check)
		return joint


	def get_conditional(self):
		counts = self.counts
		##Extend the labels.
		lan1_tags = self.lan1_tags_train.union(set(self.lan1_labels.keys()))
		lan2_tags = self.lan2_tags_train.union(set(self.lan2_labels.keys()))
		size1 = len(lan1_tags)
		size2 = len(lan2_tags)
			
		"""Change the counts into a distribution."""
		templist = []#defaultdict(  lambda: defaultdict(lambda:0))
		tempdict = {}
		
		conditionals1 =defaultdict(lambda:  defaultdict(lambda:0))
		conditionals2 =defaultdict(lambda:  defaultdict(lambda:0))

		##Should do the sanity check...
		for lan1_word in lan1_tags:
			##sanity check.
			check = 0
			on_lan1 = {}
			##if haven't seen this p(any|this word) = very very small number.
			for lan2_word in lan2_tags:
				if self.unary_counts1[lan1_word] ==0:
					conditionals1[lan1_word][lan2_word] = math.exp(-100) ####which value to assign???
					#on_lan1[lan2_word] = math.exp(-100) 
				else:
					#on_lan1[lan2_word] = 1.0*(counts[lan1_word][lan2_word] + SMOOTH)\
                                        #                                        /(self.unary_counts1[lan1_word] + size2*SMOOTH)
					conditionals1[lan1_word][lan2_word] = 1.0*(counts[lan1_word][lan2_word] + SMOOTH)\
											/(self.unary_counts1[lan1_word] + size2*SMOOTH)
					check += 1.0*(counts[lan1_word][lan2_word] + SMOOTH)\
                                                                                /(self.unary_counts1[lan1_word] + size2*SMOOTH)
			#conditionals1[lan1_word] = on_lan1
			print("Sanity check:::",lan1_word,check)
		##Repeat the thing for language two.
		
		for lan2_word in lan2_tags:
			check =0
                        ##if haven't seen this p(any|this word) = very very small number.
			for lan1_word in lan1_tags:
                                if self.unary_counts2[lan2_word] ==0:

                                        conditionals2[lan2_word][lan1_word] = math.exp(-100) ####which value to assign???
                                else:

                                        conditionals2[lan2_word][lan1_word] = 1.0*(counts[lan1_word][lan2_word] + SMOOTH)/\
					(self.unary_counts2[lan2_word] + size1*SMOOTH)
					
                                        check += 1.0*(counts[lan1_word][lan2_word] + SMOOTH)\
                                                                                /(self.unary_counts2[lan2_word] + size1*SMOOTH)


			print("Sanity check:::",lan2_word,check)
 
			##if have seen this, p(any |this word) = count(any) + E/  this_count + n*E
		
		#return conditionals1
		return conditionals1,conditionals2
	def write_to_file(self,conditional1,lan1,conditional2,lan2,sourceword):

		cond1OUT = open(sourceword + "." + lan2 + ".on." + lan1,'w') ### TODO
		cond2OUT = open(sourceword + "." + lan1 + ".on." + lan2,'w')

		for lan1_word in conditional1:
			for lan2_word in conditional1[lan1_word]:
				cond1OUT.write("{}:::{}:::{}\n".format(lan1_word,lan2_word,conditional1[lan1_word][lan2_word]))

		for lan2_word in conditional2:
                        for lan1_word in conditional2[lan2_word]:
                                cond2OUT.write("{}:::{}:::{}\n".format(lan2_word,lan1_word,conditional2[lan2_word][lan1_word]))
		cond1OUT.close()
		cond2OUT.close()

	def pickle_data(self,cond1,cond2,joint,lan1,lan2):
		cond1pname = lan2 + ".on." + lan1 + ".pickle"
		cond2pname = lan1 + ".on." + lan2 + ".pickle"
		jointpname = lan1 +"_"+ lan2 + ".joint"
		pickle.dump({1:2,3:4},open("try.p",'wb'))
		#pickle.dump(cond1,open(cond1pname,'wb'))
		pickle.dump(cond2,open(cond2pname,'wb'))
		pickle.dump(joint,open(jointpname,'wb'))

def main():
	##generate the conditionals and joint for all languages, all words.
	all_words = "bank".split()
	all_languages = sorted("it fr de".split())
	done = {}
	for word in all_words:
		for lan1 in all_languages:
			for lan2 in all_languages:
				if lan1 == lan2 or (lan1,lan2) in done or (lan2,lan1) in done:
					 continue
				else:
					print(lan1,lan2)
					cls = Occurrence(word,lan1,lan2)
					sents = cls.get_common_sents(word,lan1,lan2)
					counts = cls.get_count(sents)
					cond1,cond2 = cls.get_conditional(counts)
					joint = cls.get_joint(counts)
        				#cls.write_data(cond1,'de',cond2,'it','bank')
					#cls.pickle_data(cond1,cond2,joint,lan1,lan2)
					del cls
					done[(lan1,lan2)] = 1
	
if __name__ == "__main__":  
	#main()
	word = 'bank'
	lan1 = 'de'
	lan2 = 'fr'
	cls = Occurrence(word,lan1,lan2)
	cond1,cond2 = cls.get_conditional()
	joint = cls.get_joint()
	


		
