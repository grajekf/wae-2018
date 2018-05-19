#!/usr/bin/env bash

for E in 0 1 2
do
    for I in {1..10}
    do
        ./gen.py kawa.png -e $E -l results/kawa_e_${E}_${I}.csv -pat 10000 -b 50000
    done
done