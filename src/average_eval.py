"""
It everages the evaluations in a folder specified.
Output one file:  all.oof
		  all.best
"""

import re
import util_run_experiment
##It is averaging over all words, for each language.

def read_numbers(sourceword,targetlang,oof_best,ps,rs,mps,mrs):
	path = "../Scores/"
	fn = "{}.{}.{}.results".format(sourceword,targetlang,oof_best)
	fn = path + fn
	IN = open(fn,'r')
	lines = IN.readlines()
	line3 = lines[2]
	line5 = lines[4]
		
	p_r = re.findall('\d+\.?\d+',line3)
	mp_mr = re.findall('\d+\.?\d*',line5)

	assert len(p_r) ==2 and len(mp_mr) ==2
	p_r = [float(x) for x in p_r]
	mp_mr = [float(x) for x in mp_mr]
	ps.append(p_r[0])
	rs.append(p_r[1])
	mps.append(mp_mr[0])
	mrs.append(mp_mr[1])
	IN.close()

def calculate_avg_best_oof(targetlang,oof_best):
	path = "../Scores/"
	OUT = open(path + targetlang +"."+ oof_best + ".avg",'w')
	#all_words = util_run_experiment.final_test_words[:1]
	all_words = ["coach","education"]
	precisions = []
	recalls = []
	mprecisions = []
	mrecalls = []
	
	for word in all_words:
		read_numbers(word,targetlang,oof_best,precisions,recalls,mprecisions,mrecalls)
	avg_p = sum(precisions)/len(precisions)
	avg_r = sum(recalls)/len(recalls)
	avg_mp = sum(mprecisions)/len(mprecisions)
	avg_mr = sum(mrecalls)/len(mrecalls)

	OUT.write("{}\nAveraged Precision:{}\nAveraged Recall:{}\nAveraged Modeprecision:{}\nAveraged Moderecall{}".format(targetlang,avg_p,avg_r,avg_mp,avg_mr))	
	OUT.close()
def calculate_all():
	all_lans = "nl fr it es de".split()
	for target in all_lans:
		calculate_avg_best_oof(target,'best')
		calculate_avg_best_oof(target,'oof')

	print("All calculations are done!")


if __name__ == "__main__": calculate_all()

