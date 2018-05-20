#!/usr/bin/env bash

FILENAME="${1%%.*}"

for BS in projection
do
    for I in {1..10}
    do
        ./gen.py $1 -bs $BS -l results/${FILENAME}_bs_${BS}_${I}.csv -pat 10000 -b 50000
    done
done