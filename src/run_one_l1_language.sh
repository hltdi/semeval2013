#!/bin/bash

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export PYTHONIOENCODING=utf-8

LANG=$1
WORDS="coach education execution figure job letter match mission mood paper post pot range rest ring scene side soil strain test"

for WORD in $WORDS; do
python3 run_experiment_l1.py --targetlang="$LANG" --sourceword="$WORD" --trialdir=../trialdata/alltrials/
done
