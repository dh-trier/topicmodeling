#!/usr/bin/env python3

"""
Topic Modeling with gensim: Preprocessing.

TextBlob: https://textblob.readthedocs.io/en/dev/index.html
"""



import os
import glob
from os.path import join
from os.path import basename
from textblob import TextBlob as tb
import helpers


def load_text(textfile):
    with open(textfile, "r", encoding="utf8") as infile:
        text = infile.read()
        text = tb(text)
        return text


def prepare_text(text):
    poslist = ["NN", "NNS", "JJ", "JJR", "VB", "VBZ", "VBG", "VBN"]
    stoplist = ["date", "/date", "title", "/title", "is", "be", "been", "am", "are", "have", "has", "had", "say", "said", "make", "makes", "made", "use", "used", "do", "did", "done"]
    prepared = [item[0].lower() for item in text.tags if item[1] in poslist]
    prepared = [item for item in prepared if len(item) > 1 and item not in stoplist]
    return prepared
    

def main(workdir, dataset, identifier): 
    print("\n== preprocessing ==")
    alltextids = []
    allprepared = []
    textpath = join(workdir, "datasets", dataset, "txt", "*.txt")
    for textfile in sorted(glob.glob(textpath)):
        textid = basename(textfile).split(".")[0]
        alltextids.append(textid)
        text = load_text(textfile)
        prepared = prepare_text(text)
        allprepared.append(prepared)
        #print("done with:", textid)
    helpers.save_pickle(allprepared, workdir, identifier, "allprepared.pickle")
    print("files processed:", len(allprepared))
                          


