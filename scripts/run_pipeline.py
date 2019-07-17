#!/usr/bin/env python3

"""
Topic Modeling with gensim.
"""


# == Imports ==

from os.path import join
import preprocessing
import text2corpus
import modeling
import postprocessing
import visualization
import helpers


# == Files and folders ==


workdir = join("/", "home", "christof", "Dropbox", "5-Lehre", "2019-Sommer", "Distributional-Semantics-Riga", "")
#workdir = join("/", "media", "christof", "mydata", "Dropbox", "5-Lehre", "2019-Sommer", "Distributional-Semantics-Riga", "")
identifier = "hkpress"


# == Parameters ==

numtopics = 10
passes = 200



# == Coordinating function ==


def main(workdir, identifier):
    helpers.make_dirs(workdir, identifier)
    preprocessing.main(workdir, identifier)
    text2corpus.main(workdir, identifier)
    modeling.main(workdir, identifier, numtopics, passes)
    postprocessing.main(workdir, identifier, numtopics)
    visualization.main(workdir, identifier)
    

main(workdir, identifier)
