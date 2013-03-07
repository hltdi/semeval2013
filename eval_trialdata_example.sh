#!/bin/bash

## add -v to the end of these lines for verbose output.

perl scripts/ScorerTask3.pl L1output/bank.es.oof eval/bank.gold.es -t oof
perl scripts/ScorerTask3.pl L1output/bank.es.best eval/bank.gold.es -t best

# This will generate .result files in L1output, like bank.es.oof.result.
