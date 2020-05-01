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

import warnings
warnings.filterwarnings("ignore")



# == Files and folders ==

workdir = ".."            # working directory
dataset = "hkpress-test"  # dataset name, e.g. "hkpress-test"
identifier = "hkpt1"      # model identifier, e.g. "hkp-test-10tp"



# == Parameters ==

numtopics = 10            # number of topics of the model, e.g. 15
passes = 100              # number of iterations when modeling, eg. 500
lang = "en"               # language of the materials: "en" or "fr"



# == Coordinating function ==

def main(workdir, dataset, identifier, numtopics, passes, lang):
    helpers.make_dirs(workdir, identifier)
    preprocessing.main(workdir, dataset, identifier, lang)
    build_corpus.main(workdir, identifier)
    modeling.main(workdir, identifier, numtopics, passes)
    postprocessing.main(workdir, dataset, identifier, numtopics)
    make_overview.main(workdir, identifier) 
    
main(workdir, dataset, identifier, numtopics, passes, lang)
