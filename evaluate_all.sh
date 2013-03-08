
#!/bin/bash

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

LANGUAGES="nl de es fr it"
WORDS="coach education"
export PYTHONIOENCODING=utf-8
for LANG in $LANGUAGES; do
  for WORD in $WORDS; do
    echo "Evaluating $LANG $WORD ..."
  
    perl scripts/ScorerTask3.pl L2output/"$WORD"."$LANG".oof eval/"$WORD".gold."$LANG" -t oof
    perl scripts/ScorerTask3.pl L2output/"$WORD"."$LANG".best eval/"$WORD".gold."$LANG" -t best

  done
done










	
	
