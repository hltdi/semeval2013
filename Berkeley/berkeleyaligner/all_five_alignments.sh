#!/bin/bash

for lang in de es fr it nl; do
  ./align semeval_en_"$lang".conf
done
