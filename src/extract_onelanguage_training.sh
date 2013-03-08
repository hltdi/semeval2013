#!/bin/bash

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

TL=$1

WORDS="bank coach education execution figure job letter match mission mood  \
      movement occupation paper passage plant post pot range rest ring scene \
      side soil strain test"

export PYTHONIOENCODING=utf-8
for WORD in $WORDS; do
  echo "extracting $TL $WORD ..."
  python3 extract_training.py \
  --sourceword="$WORD" \
  --targetlang="$TL" \
  --sourcetext=/space/Europarl_Intersection_preprocessed/intersection.en.txt.ascii \
  --targettext=/space/Europarl_Intersection_preprocessed/intersection."$TL".txt \
  --alignments=/space/output_en_"$TL"/training.align \

done
