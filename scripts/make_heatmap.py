#!/usr/bin/env python3

"""
Topic Modeling with gensim: Heatmap.
"""

# == Imports ==

import os
from os.path import join
import pandas as pd
import seaborn as sns
import numpy as np


# == Parameters ==

# == Functions

def load_mastermatrix(mastermatrixfile):
    with open(mastermatrixfile, "r", encoding="utf8") as infile:
        mastermatrix = pd.read_csv(infile, sep=";")
        mastermatrix = mastermatrix.drop("Unnamed: 0", axis=1)
        #print(mastermatrix.head())
        return mastermatrix


def group_data(mastermatrix):
    mastermatrix = mastermatrix.drop(["year", "idno"], axis=1)
    data = mastermatrix.groupby(["univ"]).mean().T
    # select topics with maximum variance for visualization
    data["std"] = np.std(data, axis=1)
    data = data.sort_values(by="std", ascending=False)
    data = data.drop("std", axis=1)
    data = data.iloc[0:10,:]
    return data


def make_heatmap(data, heatmapfile):
    plot = sns.heatmap(data, linewidths=.5, annot=True, cmap="YlGnBu")
    plot.get_figure().savefig(heatmapfile, dpi=400)




# == Coordinating function ==

def main(workdir, identifier):
    print("\n== visualization2 ==")
    mastermatrixfile = join(workdir, "results", identifier, "mastermatrix.csv")
    mastermatrix = load_mastermatrix(mastermatrixfile)
    data = group_data(mastermatrix)
    heatmapfile = join(workdir, "results", identifier, "heatmap.png")
    make_heatmap(data, heatmapfile)
    print("done making heatmap")
