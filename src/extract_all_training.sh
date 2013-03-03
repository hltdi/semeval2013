#!/usr/bin/env python3

"""Given a source word, source text and target text filenames, produce training
data files."""

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, required=True)
    parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--sourcetext', type=str, required=True)
    parser.add_argument('--targettext', type=str, required=True)
    parser.add_argument('--taggerhome', type=str, required=True)
    parser.add_argument('--alignments', type=str, required=True)
    parser.add_argument('--treetaggerhome', type=str, required=False,
                        default="../TreeTagger/cmd")
    return parser

## TODO(alexr): make extract_training more modular so we can easily call it from
## this script.

def main():
    #main(sourcefn,targetfn,alignmentfn,sourceword,taggerhome,targetlang)
    all_target_languages = "nl de es fr it".split()
    all_words = "bank coach education execution figure job letter match mission mood movement occupation paper passage plant post pot range rest ring scene side soil strain test".split()
    all_words = "rest ring scene side soil strain test".split()#['ring']
    all_target_languages = ['it']
    sourcefn="/space/Europarl_Intersection_preprocessed/intersection.en.txt.ascii"
    #targetfn="/space/Europarl_Intersection_preprocessed/intersection."+targetlang+".txt"
    #alignmentfn="/space/output_en_"+targetlang+"/training.align"
    taggerhome="/home/liucan/stanford-postagger-2012-11-11" 
    
    for targetlang in all_target_languages:
        for sourceword in all_words:
            targetfn="/space/Europarl_Intersection_preprocessed/intersection."+targetlang+".txt"
            alignmentfn="/space/output_en_"+targetlang+"/training.align"
            main(sourcefn,targetfn,alignmentfn,sourceword,taggerhome,targetlang)
            print ("Done with:",sourceword,targetlang)


if __name__ == "__main__": main()
