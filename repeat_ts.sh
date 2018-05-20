#!/usr/bin/env bash

FILENAME="${1%%.*}"

for TS in 2 4 10 15 30
do
    for I in {1..10}
    do
        ./gen.py $1 -ts $TS -l results/${FILENAME}_ts_${TS}_${I}.csv -pat 10000 -b 50000
    done
done