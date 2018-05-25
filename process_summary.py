#!/usr/bin/env python3
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar="INPUT", help="Input file", type=str)
    parser.add_argument('groupby', metavar="GROUPBY", help="Group by column", type=str)
    parser.add_argument('-s', metavar="SHOW", default="Fitness function uses", help="What column to show", type=str)
    ret = parser.parse_args()
    return ret.input, ret.groupby, ret.s


inputfile, groupby, show = args()
df = pd.read_csv(inputfile)
gb = df.groupby([groupby])[show]
df_mean = gb.mean()
df_std = gb.std()
print(df_mean)
print(df_std)

matplotlib.rcParams.update({'font.size': 16})
plt.bar(np.arange(len(df_mean)), df_mean)
for i, v in enumerate(df_mean):
    plt.text(i, v + 0.25, " %.2f" % v, ha='center') 
plt.xticks(np.arange(len(df_mean)), df_mean.index)
plt.xlabel("Rozmiar turnieju")
plt.ylabel("Średnia wariancja populacji na końcu")
plt.show()

