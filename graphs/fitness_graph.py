#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import sys

BEST_FITNESS_COL = 'Best fitness'
AVG_FITNESS_COL = 'Average fitness'
MEDIAN_FITNESS_COL = 'Median fitness'
WORST_FITNESS_COL = 'Worst Fitness'
GENERATION_COL = 'Generation'


def main():
    data = pd.read_csv(sys.argv[1])
    fitness = {}
    for index, row in data.iterrows():
        best, avg, median, worst = list(row[[BEST_FITNESS_COL, AVG_FITNESS_COL, MEDIAN_FITNESS_COL, WORST_FITNESS_COL]])
        fitness[row[GENERATION_COL]] = {'best': best, 'average': avg, 'median': median, 'worst': worst}
    handles = [plt.plot(fitness.keys(), [v[name] for v in fitness.values()], label=name) for name in
               ['best', 'average', 'median', 'worst']]
    plt.legend(handles=[h[0] for h in handles], loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel('Generacja')
    plt.ylabel('Wartość funkcji celu')
    plt.show()


if __name__ == '__main__':
    main()
