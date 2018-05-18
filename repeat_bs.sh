#!/usr/bin/env bash

for BS in projection
do
    for I in {1..10}
    do
        ./gen.py kawa.png -bs $BS -l results/kawa_bs_${BS}_${I}.csv -pat 10000 -b 50000
    done
done