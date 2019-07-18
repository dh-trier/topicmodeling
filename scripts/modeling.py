#!/usr/bin/env python3

"""
Topic Modeling with gensim: Modeling.
"""

import pickle
from os.path import join
from gensim import corpora
from gensim import models
import helpers


def build_model(dictcorpus, vectorcorpus, numtopics, passes): 
    model = models.ldamodel.LdaModel(
        corpus=vectorcorpus,
        id2word=dictcorpus,
        num_topics=numtopics, 
        #random_state=100,
        update_every=1000,
        chunksize=1000,
        passes=passes,
        alpha='auto',
        eta='auto',
        #minimum_probability=0.01/numtopics,
        per_word_topics=True)
    return model

    

def main(workdir, identifier, numtopics, passes):
    print("\n== modeling ==")
    dictcorpus = helpers.load_pickle(workdir, identifier, "dictcorpus.pickle")
    vectorcorpus = helpers.load_pickle(workdir, identifier, "vectorcorpus.pickle")
    model = build_model(dictcorpus, vectorcorpus, numtopics, passes)
    helpers.save_model(workdir, identifier, model)
    print("done modeling")
    return model

