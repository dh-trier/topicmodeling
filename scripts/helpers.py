"""
Topic Modeling with gensim: helper functions.
"""

import pickle
from os.path import join
import os
from gensim import models



def make_dirs(workdir, identifier):
    picklesfolder = join(workdir, "results", identifier, "pickles", "")
    if not os.path.exists(picklesfolder):
        os.makedirs(picklesfolder)
    modelsfolder = join(workdir, "results", identifier, "model", "")
    if not os.path.exists(modelsfolder):
        os.makedirs(modelsfolder)
    wordcloudsfolder = join(workdir, "results", identifier, "wordles", "")
    if not os.path.exists(wordcloudsfolder):
        os.makedirs(wordcloudsfolder)


def save_pickle(data, workdir, identifier, picklename):
    picklesfile = join(workdir, "results", identifier, "pickles", picklename)
    with open(picklesfile, "wb") as filehandle:
        pickle.dump(data, filehandle)


def load_pickle(workdir, identifier, picklename):
    picklesfile = join(workdir, "results", identifier, "pickles", picklename)
    with open(picklesfile, "rb") as filehandle:
        data = pickle.load(filehandle)
        return data


def save_model(workdir, identifier, model):
    modelfile = join(workdir, "results", identifier, "model", identifier+".gensim")
    model.save(modelfile)


def load_model(workdir, identifier): 
    modelfile = join(workdir, "results", identifier, "model", identifier+".gensim")
    model = models.LdaModel.load(modelfile)
    return model


def load_corpus(workdir, identifier):
    corpusfile = join(workdir, "results", identifier, "pickles", "vectorcorpus.pickle")
    with open(corpusfile, "rb") as filehandle:
        corpus = pickle.load(filehandle)
        return corpus
