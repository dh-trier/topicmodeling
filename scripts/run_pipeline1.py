#!/usr/bin/env python3

"""
Topic Modeling with gensim.
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

workdir = ".."
dataset = "hkpress-test"
identifier = "hkpress-test_10t-500i"


# == Parameters ==

numtopics = 30
passes = 2000
lang = "en"


# == Coordinating function ==


def main(workdir, dataset, identifier, numtopics, passes, lang):
    helpers.make_dirs(workdir, identifier)
    preprocessing.main(workdir, dataset, identifier, lang)
    build_corpus.main(workdir, identifier)
    modeling.main(workdir, identifier, numtopics, passes)
    postprocessing.main(workdir, dataset, identifier, numtopics)
    make_overview.main(workdir, identifier) 
    
main(workdir, dataset, identifier, numtopics, passes, lang)
