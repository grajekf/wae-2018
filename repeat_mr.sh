#!/usr/bin/env bash

FILENAME="${1%%.*}"

for MR in 0.001 0.01 0.05 0.1 0.3 0.7
do
    for I in {1..10}
    do
        ./gen.py $1 -mr $MR -l results/${FILENAME}_mr${MR}_${I}.csv -pat 10000 -b 50000
    done
done