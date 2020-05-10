#!/usr/bin/env python3

"""
Topic Modeling with gensim.

This is the main coordination script.
It allows you to set the pipeline parameters.
It allows you to determine which components will be run. 
"""


# == Imports ==

from os.path import join

import helpers
import preprocessing
import build_corpus
import modeling
import postprocessing
import make_overview
import make_heatmap
import make_wordclouds
import evaluation

import warnings
warnings.filterwarnings("ignore")



# == Files and folders ==

workdir = ".."                      # working directory
dataset = "novellenschatz-test"            # dataset name
identifier = "nov-test_10t-500i"                # model identifier



# == Parameters ==

numtopics = 10                      # number of topics of the model
passes = 500                        # number of iterations when modeling
lang = "de"                         # language of the materials
cats = [["counter", "identifier", "filename"],["author"]]  # metadata categories: exclude,include



# == Coordinating function ==

def main(workdir, dataset, identifier, numtopics, passes, lang, cats):
    print("==", "starting", "==", "\n==", helpers.get_time(), "==")   
    helpers.make_dirs(workdir, identifier)
    preprocessing.main(workdir, dataset, identifier, lang)
    build_corpus.main(workdir, identifier)
    modeling.main(workdir, identifier, numtopics, passes)
    postprocessing.main(workdir, dataset, identifier, numtopics)
    make_overview.main(workdir, identifier) 
    make_heatmap.main(workdir, identifier, cats)
    make_wordclouds.main(workdir, identifier, numtopics)
    evaluation.main(workdir, identifier, numtopics)

main(workdir, dataset, identifier, numtopics, passes, lang, cats)
