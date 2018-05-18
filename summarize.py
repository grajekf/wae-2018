#!/usr/bin/env python3

import argparse
import numpy as np
import pandas as pd

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', metavar="OUTPUT", help="Output file", type=str)
    parser.add_argument('files', nargs="+", metavar="FILES", help="Files to summarize (extract the last line)", type=str)
    ret = parser.parse_args()
    return ret.output, ret.files

def main():
    output, files = args()
    dfs = [pd.read_csv(path).tail(1) for path in files]
    summary = pd.concat(dfs, ignore_index=True)
    summary.to_csv(output)



if __name__ == '__main__':
    main()