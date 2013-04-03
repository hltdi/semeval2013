#!/bin/bash 

THELANGS="de es fr it nl"
WORDS="coach education execution figure job letter match mission mood paper post pot range rest ring scene side soil strain test"

for THELANG in $THELANGS; do
  for WORD in $WORDS; do
    echo perl scripts/ScorerTask3.pl MRFoutput/"$WORD"."$THELANG".oof gold/"$THELANG"/"$WORD"_gold.txt -t oof
    perl scripts/ScorerTask3.pl MRFoutput/"$WORD"."$THELANG".oof gold/"$THELANG"/"$WORD"_gold.txt -t oof
  done
done
