#!/usr/bin/env bash

for MV in 1 5 7 10
do
    for I in {1..10}
    do
        ./gen.py kawa.png -mv $MV -l results/kawa_mv${MV}_${I}.csv -pat 10000 -b 50000
    done
done