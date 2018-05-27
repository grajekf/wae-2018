#!/usr/bin/env bash

FILENAME="${1%%.*}"

for I in {1..10}
do
    ./gen.py $1 -p 20 -ts 4 -mr 0.05 -mv 7 -l results/${FILENAME}_best_${I}.csv -pat 10000 -b 50000
done