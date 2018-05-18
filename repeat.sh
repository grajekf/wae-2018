#!/usr/bin/env bash

for P in 70 100
do
    for I in {1..10}
    do
        ./gen.py kawa.png -p $P -l results/kawa_p${P}_${I}.csv -pat 1000 -b 50000
    done
done