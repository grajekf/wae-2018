#!/usr/bin/env bash

for MR in 0.001 0.01 0.05 0.1 0.3 0.7
do
    for I in {1..10}
    do
        ./gen.py kawa.png -mr $MR -l results/kawa_mr${MR}_${I}.csv -pat 10000 -b 50000
    done
done