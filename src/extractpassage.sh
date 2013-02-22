#!/bin/bash

python3 extract_training.py \
  --sourceword=passage \
  --targetlang=de \
  --sourcetext=/space/Europarl_Intersection_preprocessed/intersection.en.txt.ascii \
  --targettext=/space/Europarl_Intersection_preprocessed/intersection.de.txt \
  --alignments=/space/output_en_de/training.align \
  --taggerhome=/home/alex/software/stanford-postagger-2012-11-11 \

