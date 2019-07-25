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


def prepare_text(text, lang):
    """
    Adds the linguistic annotation to the text: part of speech. 
    Uses the linguistic annotation to filter out certain tokens. 
    Also uses a stoplist and a minimum word length criterion to further filter tokens.
    Returns the single text as a list of lower-cased tokens. 
    """
    if lang == "en":   
        text = tb(text)
        poslist = ["NN", "NNS", "JJ", "JJR", "VB", "VBZ", "VBG", "VBN"]
        stoplist = ["date", "/date", "title", "/title", "is", "be", "been", "am", "are", "have", "has", "had", "say", "said", "make", "makes", "made", "use", "used", "do", "did", "done"]
        prepared = [item[0].lower() for item in text.tags if item[1] in poslist]
        prepared = [item for item in prepared if len(item) > 1 and item not in stoplist]
        return prepared
    elif lang == "fr":
        from textblob_fr import PatternTagger, PatternAnalyzer
        text = tb(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        poslist = ["NN", "NNS", "JJ", "JJR", "VB", "VBZ", "VBG", "VBN"]
        stoplist = ["être", "été", "est", "suis", "était", "étais", "étions", "étiez", "étaient", "sont", "sommes", "eût", "fût", "fut", "avoir", "a", "ai", "as", "avais", "avait", "avaient", "avons", "avions", "aviez", "ont", "avez", "eût", "qu", "faire", "fait", "font", "faisons", "faisez", "jusqu", "autre", "autres"]
        prepared = [item[0].lower() for item in text.tags if item[1] in poslist]
        prepared = [item for item in prepared if len(item) > 1 and item not in stoplist]
        return prepared
    else:
        print("Sorry, the language code you supplied does not refer to a supported language (en, fr).")
        print("The preprocessing step falls back to a very simple, language-agnostic procedure now.")
        print("Please consider adapting the stoplist in line 68 of \"preprocessing.py\".")
        text = re.split("\W+", text)
        prepared = [item.lower() for item in text]
        stoplist = [""]
        prepared = [item for item in prepared if len(item) > 2 and item not in stoplist]
        return prepared
        

# == Coordinating function ==

def main(workdir, dataset, identifier, lang): 
    print("\n== preprocessing ==")
    alltextids = []
    allprepared = []
    textpath = join(workdir, "datasets", dataset, "txt", "*.txt")
    for textfile in sorted(glob.glob(textpath)):
        textid = basename(textfile).split(".")[0]
        alltextids.append(textid)
        text = load_text(textfile)
        prepared = prepare_text(text, lang)
        allprepared.append(prepared)
        #print("done with:", textid)
    helpers.save_pickle(allprepared, workdir, identifier, "allprepared.pickle")
    print("files processed:", len(allprepared))
                          


