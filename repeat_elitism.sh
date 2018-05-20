#!/usr/bin/env bash

FILENAME="${1%%.*}"

for E in 0 1 2
do
    for I in {1..10}
    do
        ./gen.py $1 -e $E -l results/${FILENAME}_e_${E}_${I}.csv -pat 10000 -b 50000
    done
done