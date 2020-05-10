#!/usr/bin/env python3

"""
Topic Modeling with gensim: Preprocessing.

Provides preprocessing for the input text files. 
Adds linguistic annotation using TextBlob. 
Uses this information to filter the tokens in the documents. 
Works for English, French and German only!
For other languages, you need a different annotation tool.

See: https://textblob.readthedocs.io/en/dev/index.html
"""


# == Imports == 

import os
import glob
from os.path import join
from os.path import basename
from textblob import TextBlob as tb
import helpers
import re


# == Functions ==

def load_text(textfile):
    """
    Loads a single plain text file. 
    Provides the content as a string.
    """
    with open(textfile, "r", encoding="utf8") as infile:
        text = infile.read()
        return text


def load_stoplist(lang):
    """
    Loads a language-specific list of stopwords from the stoplists folder.
    Returns a list of stopwords.
    """
    try: 
        stoplistfile = join("stoplists", lang+".txt")
        with open(stoplistfile, "r", encoding="utf8") as infile:
            stoplist = infile.read().split("\n")
        return stoplist
    except:
        stoplist = []
        print("Warning. No stoplist for the indicated language has been found.")
        print("Please consider adding a stoplist for the language code to the stoplist folder.")
        return stoplist


def prepare_text(text, lang, stoplist):
    """
    Adds the linguistic annotation to the text: part of speech. 
    Uses the linguistic annotation to filter out certain tokens.
    By default, nouns, verbs and adjectives are retained.
    Also uses a stoplist and a minimum word length criterion to further filter tokens.
    Returns the single text as a list of lower-cased tokens.
    """
    if lang == "en":   
        text = tb(text)
        poslist = ["NN", "NNS", "JJ", "JJR", "VB", "VBZ", "VBG", "VBN"]
        prepared = [item[0].lower() for item in text.tags if item[1] in poslist]
        prepared = [item for item in prepared if len(item) > 1 and item not in stoplist]
        return prepared
    elif lang == "fr":
        from textblob_fr import PatternTagger, PatternAnalyzer
        text = tb(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        poslist = ["NN", "NNS", "JJ", "JJR", "VB", "VBZ", "VBG", "VBN"]
        prepared = [item[0].lower() for item in text.tags if item[1] in poslist]
        prepared = [item for item in prepared if len(item) > 1 and item not in stoplist]
        return prepared
    elif lang == "de":
        from textblob_de import TextBlobDE as tbd
        text = tbd(text)
        poslist = ["NN", "NNS", "JJ", "JJR", "VB", "VBZ", "VBG", "VBN"]
        prepared = [item[0].lower() for item in text.tags if item[1] in poslist]
        prepared = [item for item in prepared if len(item) > 1 and item not in stoplist]
        #print(prepared[0:100])
        return prepared
    else:
        print("Sorry, the language code you supplied does not refer to a supported language (en, de, fr).")
        print("The preprocessing step falls back to a very simple, language-agnostic procedure now.")
        print("Please consider adding a stoplist for your language code.")
        text = re.split("\W+", text)
        prepared = [item.lower() for item in text]
        prepared = [item for item in prepared if len(item) > 2 and item not in stoplist]
        return prepared
        

# == Coordinating function ==

def main(workdir, dataset, identifier, lang): 
    print("\n== preprocessing ==")
    alltextids = []
    allprepared = []
    stoplist = load_stoplist(lang)
    textpath = join(workdir, "datasets", dataset, "txt", "*.txt")
    for textfile in sorted(glob.glob(textpath)):
        textid = basename(textfile).split(".")[0]
        alltextids.append(textid)
        text = load_text(textfile)
        prepared = prepare_text(text, lang, stoplist)
        allprepared.append(prepared)
        #print("done with:", textid)
        #print(prepared[0:10])
    helpers.save_pickle(allprepared, workdir, identifier, "allprepared.pickle")
    print("files processed:", len(allprepared))
    print("==", helpers.get_time(), "done preprocessing", "==")   

                          


