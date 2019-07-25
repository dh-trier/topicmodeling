#!/usr/bin/env python3

"""
Topic modeling with gensim: make wordclouds.

Creates a wordcloud for each topic in the model. 

See: https://amueller.github.io/word_cloud/
"""


# == imports ==

import os
import glob
from os.path import join
import re
import pandas as pd
import wordcloud
from matplotlib import cm


# == Functions == 

def load_allwordprobs(wordprobsfile):
    with open(wordprobsfile, "r", encoding="utf8") as infile: 
        allwordprobs = pd.read_csv(infile, sep="\t", index_col=0)
        return allwordprobs


def get_wcl(fontfile): 
    wcl = wordcloud.WordCloud(
        font_path=fontfile,
        width = 800, 
        height = 500, 
        scale = 2,
        margin = 20,
        prefer_horizontal = 0.95,
        background_color='white',
        color_func = lambda *args, **kwargs: (15, 52, 112)
        )
    return wcl


def get_wordprobs(i, allwordprobs, numwords): 
    allwordprobs = allwordprobs.sort_values(by=str(i), axis=0, ascending=False)
    words = allwordprobs.index[0:numwords]
    probs = list(allwordprobs.iloc[0:numwords,i])
    probs = [prob*100 for prob in probs]
    wordprobs = dict(zip(words, probs))
    return wordprobs


def make_wordcloud(wcl, wordprobs, filename): 
    wclobject = wcl.generate_from_frequencies(wordprobs)
    #wclobject.recolor(colormap=cm.viridis)
    wclobject.to_file(filename)
    

# == Coordinating function == 

def main(workdir, identifier, numtopics):
    print("\n== make_wordclouds ==")
    wordprobsfile = join(workdir, "results", identifier, "wordprobs.csv")
    wordcloudsfolder = join(workdir, "results", identifier, "wordles", "")
    fontfile = "Ubuntu-M.ttf"
    allwordprobs = load_allwordprobs(wordprobsfile)    
    wcl = get_wcl(fontfile)
    for i in range(0, numtopics): 
        wordprobs = get_wordprobs(i, allwordprobs, numwords=40)
        filename = join(wordcloudsfolder, "topic_"+'{:03}'.format(i+1)+".png")
        #print(i+1)
        make_wordcloud(wcl, wordprobs, filename)
    print("finished making wordclouds")

