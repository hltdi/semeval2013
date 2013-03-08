#!/usr/bin/env python3

"""Build all 25 * 5 classifiers and pickle them. Mostly built by liucan;
refactored by alexr."""

import pickle
import nltk
import sys

from train_from_extracted import get_maxent_classifier
import util_run_experiment
def main():
    lan = sys.argv[1]
    ## all_target_languages = "nl de es fr it".split()
    all_target_languages = [lan]
    all_words = "bank coach education execution figure job letter match mission mood movement occupation paper passage plant post pot range rest ring scene side soil strain test".split()
    assert len(all_words) == 25
    #assert len(all_target_languages) == 5

    nltk.classify.megam.config_megam(bin='/usr/local/bin/megam')
    for sourceword in all_words:
        for target in all_target_languages:
            print("Training {0}/{1}".format(sourceword, target))
            classifier = get_maxent_classifier(sourceword, target)
            picklefn = \
                "../L1pickle/{0}.{1}.level1.pickle".format(sourceword, target)
            with open(picklefn, "wb") as outfile:
                pickle.dump(classifier, outfile)

if __name__ == "__main__": main()
