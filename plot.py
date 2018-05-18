#!/usr/bin/env python3
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


dfs = [pd.concat([pd.read_csv(f"results/population/kawa_p{i}_{j}.csv")for j in range(1, 11)], ignore_index=True) for i in [10,20,40,70,100]]

gbs = [df.groupby(["Fitness function uses"]) for df in dfs]
dfs_mean = [gb["Best fitness"].mean() for gb in gbs]
dfs_std = [gb["Best fitness"].std() for gb in gbs]

# print(len(dfs))

# xs = [df["Fitness function uses"] for df in dfs]
# ys = [df["Best fitness"] for df in dfs]

for x,y,i in zip([df.index for df in dfs_mean], dfs_mean, [10,20,40,70,100]):
    plt.plot(x, y, label=f"Rozmiar populacji: {i}")
plt.legend(loc='lower right')

plt.show()