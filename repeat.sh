#!/usr/bin/env bash

FILENAME="${1%%.*}"

for P in 10 20 40 70 100
do
    for I in {1..10}
    do
        ./gen.py $1 -p $P -l results/${FILENAME}_p${P}_${I}.csv -pat 1000 -b 50000
    done
done