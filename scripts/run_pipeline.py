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
import make_heatmap
import make_wordclouds
import evaluation

import warnings
warnings.filterwarnings("ignore")


# == Files and folders ==

workdir = ".."
dataset = "hkpress-test"
identifier = "hkpress-test_10t-500i"


# == Parameters ==

numtopics = 10
passes = 500


# == Coordinating function ==


def main(workdir, dataset, identifier):
    helpers.make_dirs(workdir, identifier)
    preprocessing.main(workdir, dataset, identifier)
    build_corpus.main(workdir, identifier)
    modeling.main(workdir, identifier, numtopics, passes)
    postprocessing.main(workdir, dataset, identifier, numtopics)
    make_overview.main(workdir, identifier) 
    make_heatmap.main(workdir, identifier)
    make_wordclouds.main(workdir, identifier, numtopics)
    evaluation.main(workdir, identifier, numtopics)
    

main(workdir, dataset, identifier)
