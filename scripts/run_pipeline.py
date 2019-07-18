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

import warnings
warnings.filterwarnings("ignore")


# == Files and folders ==

#workdir = join("/", "home", "christof", "Dropbox", "5-Lehre", "2019-Sommer", "Distributional-Semantics-Riga", "")
workdir = join("/", "media", "christof", "mydata", "Dropbox", "5-Lehre", "2019-Sommer", "Distributional-Semantics-Riga", "")
dataset = "hkpress"
identifier = "hkpress_50t-4000i"


# == Parameters ==

numtopics = 50
passes = 4000


# == Coordinating function ==


def main(workdir, dataset, identifier):
    helpers.make_dirs(workdir, identifier)
    preprocessing.main(workdir, dataset, identifier)
    build_corpus.main(workdir, identifier)
    modeling.main(workdir, identifier, numtopics, passes)
    postprocessing.main(workdir, dataset, identifier, numtopics)
    make_overview.main(workdir, identifier) #slow#
    make_heatmap.main(workdir, identifier)
    make_wordclouds.main(workdir, identifier, numtopics)
    

main(workdir, dataset, identifier)
