#!/usr/bin/env python3
import pandas as pd
import numpy as np
import argparse


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar="INPUT", help="Input file", type=str)
    parser.add_argument('groupby', metavar="GROUPBY", help="Group by column", type=str)
    ret = parser.parse_args()
    return ret.input, ret.groupby


inputfile, groupby = args()
df = pd.read_csv(inputfile)
gb = df.groupby([groupby])["Fitness function uses"]
df_mean = gb.mean()
df_std = gb.std()
print(df_mean)
print(df_std)

