#!/usr/bin/env python3

"""
Topic Modeling with gensim.
"""


# == Imports ==

import os
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


# == Base parameters == 

import warnings
warnings.filterwarnings("ignore")
workdir = join(os.path.realpath(os.path.dirname(__file__)), "..")


# == Files, folders, s ==

dataset = "hkpress"                     # see folder 'datasets'
lang = "en"                             # en|fr|de
identifier = "progress"                 # freely defined label 


# == Parameters ==

#cats = [["id", "filename", "title", "year"],["author"]] # Novellenschatz
cats = [["year"],["univ"]] # hkpress
numtopics = 10                          
passes = 200


# == Coordinating function ==


def main(workdir, dataset, identifier):
    print("== starting ==\n==", helpers.get_time(), "==")   
    helpers.make_dirs(workdir, identifier)
    preprocessing.main(workdir, dataset, identifier, lang)
    build_corpus.main(workdir, identifier)
    modeling.main(workdir, identifier, numtopics, passes)
    #postprocessing.main(workdir, dataset, identifier, numtopics)
    #make_overview.main(workdir, identifier) 
    #make_heatmap.main(workdir, identifier, cats)
    #make_wordclouds.main(workdir, identifier, numtopics)
    #evaluation.main(workdir, identifier, numtopics)
    

main(workdir, dataset, identifier)




"""

The variable "cats" has the structure "[[exclude],[include]]". 
It serves to include and exclude certain metadata categories from the heatmap visualisation.

for hkpress, e.g.: 
cats = [["year"],["univ"]]

for Novellenschatz, e.g.:  
cats = [["counter", "identifier", "filename"],["author"]]  


"""