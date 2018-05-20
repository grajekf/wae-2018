#!/usr/bin/env bash

FILENAME="${1%%.*}"

for MV in 1 5 7 10
do
    for I in {1..10}
    do
        ./gen.py $1 -mv $MV -l results/${FILENAME}_mv${MV}_${I}.csv -pat 10000 -b 50000
    done
done