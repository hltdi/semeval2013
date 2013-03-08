#!/usr/bin/env python3

"""Given a source word, source text and target text filenames, produce training
data files."""

import sys
import os
import argparse
import functools
import re

import nltk
from nltk.stem import wordnet

import get_possible_senses
import treetagger
from Aligner import target_words_for_each_source_word
from Aligner import source_words_for_each_target_word
from Aligner import source_indices_for_each_target_word
from Aligner import sort_alignment

wnl = wordnet.WordNetLemmatizer()

## These are all the kinds of nouns present in WSJ tagsets.
NOUN = {'NN','NNS','NNP','NP','NNPS','NPS'}
LIKELY_NP = {'JJ','JJR','JJS','POS','DT','NN','NNS','NNP','NP','NNPS','NPS'}
def keep_candidate(candidate, sourceword):
    """Decide whether to keep a candidate based on its tagged source
    sentence."""
    ## now check whether we have the source word as a noun...
    for word,tag in candidate.source_tagged:
        if tag in NOUN:
            if wnl.lemmatize(word.lower()) == sourceword:
                return True
    return False

def load_bitext(sourcefn, targetfn, alignfn, sourceword):
    """Return four lists of sentence-like things. First source, then
    target, then alignment, then tagged source."""
    pretaggedfn = sourcefn + ".pretagged"
    pat = re.compile(r".*"+sourceword+".*", flags=re.IGNORECASE)
    out_source = []
    out_target = []
    out_align = []
    out_st = []
    count = 0
    with open(sourcefn) as infile_s, \
         open(targetfn) as infile_t, \
         open(alignfn) as infile_align, \
         open(pretaggedfn) as infile_st:
        for source, target, alignment, st in \
            zip(infile_s, infile_t, infile_align, infile_st):
            if re.match(pat, source):
                out_source.append(source.strip())
                out_target.append(target.strip())
                out_align.append(alignment.strip())
                out_st.append(st.strip())
                count += 1
                ## if count == 200: break
    return out_source, out_target, out_align, out_st

def lemmatize_sentence(sentence, language, tt_home=None):
    """For a tokenized sentence in the given language, call TreeTagger on it to
    get a list of lemmas."""
    codes_to_names = {"en":"english", "de":"german", "it":"italian",
                      "es":"spanish", "fr":"french", "nl":"dutch"}
    tt_lang = codes_to_names[language]
    tt = treetagger.TreeTagger(tt_home=tt_home, language=tt_lang)
    output = tt.tag(sentence)
    return [lemma.lower() for word,tag,lemma in output]

def batch_lemmatize_sentences(sentences, language, tt_home=None):
    """For a list of tokenized sentences in the given language, call TreeTagger
    on them to get a list of lemmas; lowercase them all."""
    codes_to_names = {"en":"english", "de":"german", "it":"italian",
                      "es":"spanish", "fr":"french", "nl":"dutch"}
    tt_lang = codes_to_names[language]

    if tt_lang == 'english':
        tt = treetagger.TreeTagger(tt_home=tt_home,
                                   language=tt_lang,
                                   encoding='latin-1')
    else:
        tt = treetagger.TreeTagger(tt_home=tt_home, language=tt_lang)
    output = tt.batch_tag(sentences)
    return [[lemma.lower() for word,tag,lemma in sent] for sent in output]

def list_has_sublist(biglist, sublist):
    """We could use this to look for known target-language senses in the target
    text. Possibly fall back to this if we can't find a good target-language
    sense with the alignments? Return the index of the sublist, if it's present,
    otherwise False."""
    size = len(sublist)
    for pos in range(len(biglist) - len(sublist) + 1):
        maybe = biglist[pos:pos+size]
        if maybe == sublist:
            return pos
    return False

class TrainingCandidate:
    def __init__(self, source_line, target_line, alignment_line):
        self.source_line = source_line.strip()
        self.target_line = target_line.strip()
        self.alignment_line = alignment_line.strip()

        self.target_tokenized = self.target_line.split()
        self.source_tokenized = self.source_line.split()

        # fill in later
        self.source_tagged = None
        self.target_lemmatized = None
        self.source_lemmatized = None

def batch_lemmatize(candidates, targetlang, tt_home):
    """For each candidate, lemmatize the sentences and stick that information on
    the candidate objects."""
    ## target language
    sents = [candidate.target_tokenized for candidate in candidates]
    lemmatized_sentences = batch_lemmatize_sentences(sents, targetlang, tt_home)
    assert len(lemmatized_sentences) == len(sents)
    for candidate,lemmas in zip(candidates, lemmatized_sentences):
        candidate.target_lemmatized = lemmas

    ## source language
    sents = [candidate.source_tokenized for candidate in candidates]
    lemmatized_sentences = batch_lemmatize_sentences(sents, "en", tt_home)
    assert len(lemmatized_sentences) == len(sents)
    for candidate,lemmas in zip(candidates, lemmatized_sentences):
        candidate.source_lemmatized = lemmas

contractions = \
"l' d' dell' un' all' dall' nell' sull'".split()
def strip_initial_contraction(label):
    """Strip out l' and d' (fr) and dell' (it), etc."""
    normalized_label = label.replace("’", "'")
    for contraction in contractions:
        if normalized_label.startswith(contraction):
            out = normalized_label[len(contraction):]
            print("CONTRACTION DETECTED", label, contraction)
            print("STRIPPED TO", out)
            return out
    return label

import string
punctuations = string.punctuation + "«»¡"

def strip_edge_punctuation(label):
    """Strip out punctuation along the edges. It's pretty bad if this gets into
    the training data."""
    for punc in punctuations:
        if label.startswith(punc):
            print("STRIPPED", punc, "FROM", label)
            label = label[1:]
        if label.endswith(punc):
            print("STRIPPED", punc, "FROM", label)
            label = label[:1]
    return label

def print_candidate_to_file(candidate, index, label, outfile):
    """Given a candidate object, the index of the head word in the source
    language, and the label we want to mark it with, print it into the
    outfile."""
    withtags = map(nltk.tag.tuple2str, candidate.source_tagged)
    withtags = list(withtags)
    tagged = " ".join(withtags)
    ## print the tagged source context.
    print(tagged, file=outfile)
    ## print the index of the head word.
    print(index, file=outfile) ## index of source word
    ## print the label
    assert "<unknown>" not in label
    label = strip_initial_contraction(label)
    label = strip_edge_punctuation(label)
    if label:
        print(label, file=outfile)

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--sourceword', type=str, required=True)
    parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--sourcetext', type=str, required=True)
    parser.add_argument('--targettext', type=str, required=True)
    parser.add_argument('--alignments', type=str, required=True)
    parser.add_argument('--treetaggerhome', type=str, required=False,
                        default="../TreeTagger/cmd")
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    sourcefn = args.sourcetext
    targetfn = args.targettext
    alignmentfn = args.alignments
    sourceword = args.sourceword
    all_target_languages = "de es fr it nl".split()
    assert args.targetlang in all_target_languages
    targetlang = args.targetlang
    tt_home = args.treetaggerhome

    out_fn = "../trainingdata/{0}.{1}.train".format(sourceword, targetlang)

    ## load up all the preprocessed and aligned data.
    source_lines, target_lines, alignment_lines, sourcetag_lines = \
        load_bitext(sourcefn, targetfn, alignmentfn, sourceword)
    print("got source/target lines")
    assert(len(set([len(source_lines), len(target_lines), len(alignment_lines),
                   len(sourcetag_lines)])) == 1)

    gold_labels = get_possible_senses.senses(sourceword, targetlang)
    labelwords_by_len = sorted([label.split() for label in gold_labels],
                               key=len,
                               reverse=True)
    lemmatized_labels = set()
    unlemmatized_labels = set()

    candidates = []
    for sl, tl, al in zip(source_lines, target_lines, alignment_lines):
        candidates.append(TrainingCandidate(sl,tl,al))

    ## tag it up.
    for candidate,st in zip(candidates, sourcetag_lines):
        tagged_sent = list(map(nltk.tag.str2tuple, st.split()))
        candidate.source_tagged = tagged_sent

    ## having listed the candidates, filter them down.
    make_into_training_data = []
    for candidate in candidates:
        if keep_candidate(candidate, sourceword):
            make_into_training_data.append(candidate)

    ## lemmatize remaining candidates for both languages.
    batch_lemmatize(make_into_training_data, targetlang, tt_home)

    with open(out_fn, "w") as outfile:
        for candidate in make_into_training_data:
            found = False
            tags = [tag for (word,tag) in candidate.source_tagged]
            alignment = sort_alignment(candidate.alignment_line).split()
            tws = target_words_for_each_source_word(candidate.source_lemmatized,
                                                    candidate.target_lemmatized,
                                                    alignment)
            tws2 = target_words_for_each_source_word(candidate.source_lemmatized,
                                                     candidate.target_tokenized,
                                                     alignment)
            source_lemmas = candidate.source_lemmatized
            target_lemmas = candidate.target_lemmatized

            ## look for the known gold labels.
            target_lower = [tok.lower() for tok in candidate.target_tokenized]
            for labelwords in labelwords_by_len:
                label = " ".join(labelwords)
                found_in_lemmatized = False
                start = list_has_sublist(target_lemmas, labelwords)
                if start: found_in_lemmatized = True
                if not start:
                    start = list_has_sublist(target_lower, labelwords)
                if not start: continue
                sws = source_words_for_each_target_word(
                    candidate.source_lemmatized, target_lemmas, alignment)
                source_indices = source_indices_for_each_target_word(
                    candidate.source_lemmatized, target_lemmas, alignment)
                for i in range(start, start+len(labelwords)):
                    if sourceword in sws[i]:
                        subindex = sws[i].index(sourceword)
                        source_index = source_indices[i][subindex]
                        found = True
                        if found_in_lemmatized:
                            lemmatized_labels.add(label)
                        else:
                            unlemmatized_labels.add(label)
                        print_candidate_to_file(candidate, source_index, label,
                                                outfile)
                if found: break

                ## the target sense is here in the target language, but
                ## there's nothing aligned to the source word, we'll take a
                ## guess. (good idea? maybe?)
                for i in range(len(tags)):
                    if (source_lemmas[i] == sourceword and
                        tags[i] in NOUN and
                        not tws[i]):
                        print_candidate_to_file(candidate, i, label, outfile)
                        if found_in_lemmatized:
                            lemmatized_labels.add(label)
                        else:
                            unlemmatized_labels.add(label)

            ## if we found a gold label for this candidate, go to next
            ## candidate! XXX(alexr): good idea? Or maybe we should allow
            ## several training examples to be extracted?
            if found: continue

            ## scan using the alignments.
            for i in range(len(tags)):
                has_alignment = bool(tws[i])
                if not has_alignment: continue
                l_label = " ".join(tws[i]).lower()
                u_label = " ".join(tws2[i]).lower()

                ## Case where we found the right word.
                if (source_lemmas[i] == sourceword and tags[i] in NOUN):
                    lemmatized_labels.add(l_label)
                    unlemmatized_labels.add(u_label)
                    if ("<unknown>" not in l_label and
                        "@" not in l_label and
                        "|" not in l_label):
                        print_candidate_to_file(candidate, i, l_label, outfile)
                    else:
                        print_candidate_to_file(candidate, i, u_label, outfile)
                ## But maybe we are in the right noun phrase and the word 
                ## word aligned to us is one of the known senses:
                ## include that too.
                if tags[i] in LIKELY_NP:
                    found_source = False
                    offset = 0
                    for off in [-2, -1, 1, 2]:
                        if (i + off) in range(len(tags)):
                            if (source_lemmas[i+off] == sourceword and
                                tags[i+off] in NOUN):
                                offset = off
                                found_source = True
                                break
                    if found_source:
                        if l_label in gold_labels:
                            lemmatized_labels.add(l_label)
                            print_candidate_to_file(candidate,
                                                    i+offset,
                                                    l_label,
                                                    outfile)
                        elif u_label in gold_labels:
                            unlemmatized_labels.add(u_label)
                            print_candidate_to_file(candidate,
                                                    i+offset,
                                                    u_label,
                                                    outfile)

    all_seen_labels = lemmatized_labels.union(unlemmatized_labels)
    unseen_labels = gold_labels - all_seen_labels
    nonstandard_labels = all_seen_labels - gold_labels
    print("*" * 80)
    print("observed labels", sorted(list(all_seen_labels)))
    print("*" * 80)
    print("nonstandard labels", sorted(list(nonstandard_labels)))
    print("*" * 80)
    print("unseen gold labels", sorted(list(unseen_labels)))

if __name__ == "__main__": main()
