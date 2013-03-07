"""
This file gets the co-occurrence table for languages.
1. Just count
2. A distribution from the count
3. co-occurrence distri and classifier output on the same scale.
"""
import math
import pickle
import sys
import functools
from collections import defaultdict
### import the alignment file.
SMOOTH = 0.002

class Occurrence:

	def __init__(self,sourceword,lan1,lan2):
		self.sent_pairs = []
		self.cooccur = defaultdict(  lambda: defaultdict (lambda:0))
		self.lan1_labels = set()
		self.lan2_labels = set()
		self.lan1_tags_train = set()
		self.lan2_tags_train = set()
		self.unary_counts1 = defaultdict(lambda:0)
		self.unary_counts2 = defaultdict(lambda:0)
		self.sent_pairs = []
		self.counts = {} 
		#cls = Occurrence(word,lan1,lan2)
		self.get_common_sents(sourceword,lan1,lan2,False)
		self.get_count()
		self.lan1 = lan1
		self.lan2 = lan2

	def get_common_four_sents(self,word,lan1,lan2,lan3,lan4):

		###NOTE:  this functions returns a list of each sentence. Because of the duplicates. Also duplicate the training in				stances in these cases.
		lan1_lan2 = self.get_common_sents(word,lan1,lan2,True)
		lan3_lan4 = self.get_common_sents(word,lan3,lan4,True)
		
		intersection = {}  ##this returns mappings of the form, (sentence) --> (l1,l2,l3,l4). Useful later on. 
		for sentence in lan1_lan2:
			if sentence in lan3_lan4:
				##if this sentence in contained in both, then put (sentence) --> (l1,l2,l3,l4)
				pairs12 = lan1_lan2[sentence]
				pairs34 = lan3_lan4[sentence]
				#quadruple = (pair12[0],pair12[1],pair34[0],pair34[1])
				quadruples = self.duplicate_quadruple(pairs12,pairs34)
				intersection[sentence] = quadruples


		print("##### 1 and 2",len(lan1_lan2))
		print("##### 3 and 4",len(lan3_lan4))
		print("##### all intersect:",len(intersection))		
		#for key in intersection:
			#print("{}#####\n####{}".format(key,intersection[key]))
		#	print(key)
		print(lan1,lan2,lan3,lan4)
	
		return intersection
	def duplicate_pair(self,left,right):
		##left is a list of items, and right is a list of item. Return the Cardian Product of left and right.
		result = []
		for item_l in left:
			for item_r in right:
				result.append((item_l,item_r))

		return list(set(result))

	def duplicate_quadruple(self,left_pairs,right_pairs):
		pairs1 = [x[0] for x in left_pairs]
		pairs2 = [x[1] for x in left_pairs]
		pairs3 = [x[0] for x in right_pairs]
		pairs4 = [x[1] for x in right_pairs]

		quadruples = []
		for item1 in pairs1:
			for item2 in pairs2:
				for item3 in pairs3:
					for item4 in pairs4:
						quadruples.append( (item1,item2,item3,item4)   )

		return list(set(quadruples))

	def get_common_sents(self,sourceword,lan1,lan2,level2Mode):
		path = "../trainingdata/"
		lan1FN = path+sourceword +"."+ lan1 + ".train"
		lan2FN = path+sourceword +"."+ lan2 + ".train"
		
		IN1 = open(lan1FN,'r')
		IN2 = open(lan2FN,'r')
		
		line1 = IN1.readline()
		line2 = IN2.readline()
		dic1 = defaultdict(lambda:0)
		dic2 = defaultdict(lambda:0)
		duplicates1 = defaultdict(lambda: [])
		duplicates2 = defaultdict(lambda: [])
		count = 1
		triple = []
		mappings1 = {}
		mappings2 = {}
		while line1:
			
			triple.append(line1.strip())
			if count %3 ==1: pass ##add this sentence to 
				#dic1[line1.strip()] +=1
			if count%3==0:  ##It is the end of a sentence
				##mappings1[triple[0]] = (triple[2])
				##the old key is just sentence. Since sentences are not unique, 
				##we should use sentence_index as the unique key, hopefully sentence_index don't have
				##too many repeats.
				assert (triple[2] == triple[2].lower())
				mappings1["{}####{}".format(triple[0],triple[1])] = (triple[2])
				duplicates1["{}####{}".format(triple[0],triple[1])].append(triple[2])
				dic1["{}####{}".format(triple[0],triple[1])] +=1
				triple = []
			count+=1
			line1 = IN1.readline()

		count = 1
		triple = []
		while line2:
			
			triple.append(line2.strip())
			if count %3 ==1: pass ##add this sentence to s
				#dic2[line2.strip()] +=1
			if count%3==0:	
				assert (triple[2] == triple[2].lower())
				#mappings2[triple[0]] = (triple[2])
				mappings2["{}####{}".format(triple[0],triple[1])] = (triple[2])
				duplicates2["{}####{}".format(triple[0],triple[1])].append(triple[2])
				dic2["{}####{}".format(triple[0],triple[1])] +=1
				triple = []
			count +=1
			line2 = IN2.readline()
		
		##Finding the intersection of the two dictionaries.
		total = 0
		count = 0
		sent_pairs = []
		sents_for_level2 = {}
		for key in dic1:
			if key in dic2:
				
				if dic1[key] == dic2[key] == 1: ###the simple case, where we can just append the mappings.
					pair = (mappings1[key],mappings2[key])
					self.collect_data([pair])
					sent_pairs.append(pair)
					if level2Mode:  sents_for_level2[key] = [pair]
				else:  ##we need to duplicate data: either lan1 or lan2 have unsure alignments. 
					##First get the actual alignments for each language, and make the product
					duplicate_items1 = duplicates1[key]
					duplicate_items2 = duplicates2[key]
					pairs = self.duplicate_pair(duplicate_items1,duplicate_items2)
					self.collect_data(pairs)
					sent_pairs.extend(pairs)	
					if level2Mode: sents_for_level2[key] = pairs  ##The sentence, with lan1,lan2 word.
					##need to change the function in level2.				

				total += dic2[key]
				count +=1

		print("Total overlapped sents:",total,count)
		self.sent_pairs = sent_pairs
		for key in dic2:
			if dic2[key]>1: print("It is duplicated!!!",key,duplicates2[key])
		if level2Mode: return sents_for_level2

	def collect_data(self,pairs):
		for pair in pairs:
			self.lan1_tags_train.add(pair[0])
			self.lan2_tags_train.add(pair[1])
			self.unary_counts1[pair[0]] +=1
			self.unary_counts2[pair[1]] +=1

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
		lan1_tags = self.lan1_tags_train
		lan2_tags = self.lan2_tags_train
		total = sum( [ sum( list(counts[w1].values()  ) ) for w1 in counts ] )
		##joint probability.
		joint = {}
		check = 0
		for lan1_word in lan1_tags:
			for lan2_word in lan2_tags:
				joint_p = 1.0* (  SMOOTH + counts[lan1_word][lan2_word]  ) / (total + SMOOTH*len(lan1_tags)*len(lan2_tags))
				key = (lan1_word +"_"+self.lan1+"&&"+lan2_word+"_"+self.lan2)
				## make sure all labels are lowercased.
				key = key.lower()
				joint[key] = joint_p
				#joint[(lan2_word +"&&"+lan1_word)] = joint_p
				check += joint_p

		print (check)
		return joint


	def get_conditional(self):
		counts = self.counts
		##Extend the labels.
		lan1_tags = self.lan1_tags_train
		lan2_tags = self.lan2_tags_train
		lan1_tags = [tag.lower() for tag in lan1_tags]
		lan2_tags = [tag.lower() for tag in lan2_tags]
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

	@functools.lru_cache(maxsize=10000)
	def lookup_joint(self,lan1,word_lan1,lan2,word_lan2):
		if (self.lan1 == lan2) and (self.lan2 == lan1):
			lan2,lan1 = lan1,lan2
			word_lan1,word_lan2 = word_lan2,word_lan1
		key = "{}_{}&&{}_{}".format(word_lan1,lan1,word_lan2,lan2)
		dic = self.get_joint()
		return dic[key]

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
					sents = cls.get_common_sents(word,lan1,lan2,False)
					counts = cls.get_count(sents)
					cond1,cond2 = cls.get_conditional(counts)
					joint = cls.get_joint(counts)
        				#cls.write_data(cond1,'de',cond2,'it','bank')
					#cls.pickle_data(cond1,cond2,joint,lan1,lan2)
					del cls
					done[(lan1,lan2)] = 1
	
if __name__ == "__main__":  
	#main()
	#word = 'rest'
	word = sys.argv[1]
	lan1 = 'it'
	lan2 = 'es'
	lan3 = 'fr'
	lan4 = 'nl'
	cls = Occurrence(word,lan1,lan2)
	#print(cls.duplicate_pair(['a','f'],['b','c','e']))
	cond1,cond2 = cls.get_conditional()
	joint = cls.get_joint()
	print(cls.lookup_joint('it','banca','es','banco'))
	print(cls.lookup_joint('es','banco','it','banca'))
	print(cls.lookup_joint('it','banca','de','bank'))
	#sent_l2 = cls.get_common_sents(word,lan1,lan2,True)
	#for key in joint:
	#	print(key,"   :::  ",joint[key],"\n")
	#kkk = cls.get_common_four_sents(word,lan1,lan2,lan3,lan4)


		
