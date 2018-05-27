#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys

CLASS_NAME_COL = 'Predicted class {}'
CLASS_PROB_COL = 'Probability {}'
# CLASS_PROB_COL = 'Predicted class {}'
# CLASS_NAME_COL = 'Probability {}'
GENERATION_COL = 'Generation'


def main():
    filename = sys.argv[1]
    data = pd.read_csv(filename)

    class_names = list(set([item for i in range(5) for item in list(
        data[CLASS_NAME_COL.format(i + 1)].unique())]))

    probabilities = {}

    for index, row in data.iterrows():
        class_probs = dict([(name, 0) for name in class_names])
        for i in range(5):
            class_name, prob = row[[CLASS_NAME_COL.format(
                i + 1), CLASS_PROB_COL.format(i + 1)]]
            class_probs[class_name] = prob
        probabilities[row[GENERATION_COL]] = class_probs
    # print(class_names)
    handles = [plt.plot(probabilities.keys(), [v[name] for v in probabilities.values()], label=name) for name in
               class_names]
    plt.legend(handles=[h[0] for h in handles])  # ,
    # loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel('Generacja')
    plt.ylabel('Prawdopodobieństwo klasy')
    plt.show()


if __name__ == '__main__':
    main()
