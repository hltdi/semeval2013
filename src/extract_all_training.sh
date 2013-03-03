#!/bin/bash

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

LANGUAGES="nl de es fr it"
WORDS="bank coach education execution figure job letter match mission mood  \
      movement occupation paper passage plant post pot range rest ring scene \
      side soil strain test"

export PYTHONIOENCODING=utf-8
for LANG in $LANGUAGES; do
  for WORD in $WORDS; do
    echo "extracting $LANG $WORD ..."
    python3 extract_training.py \
    --sourceword="$WORD" \
    --targetlang="$LANG" \
    --sourcetext=/space/Europarl_Intersection_preprocessed/intersection.en.txt.ascii \
    --targettext=/space/Europarl_Intersection_preprocessed/intersection."$LANG".txt \
    --alignments=/space/output_en_"$LANG"/training.align \
    --taggerhome=/home/liucan/stanford-postagger-2012-11-11

  done
done

