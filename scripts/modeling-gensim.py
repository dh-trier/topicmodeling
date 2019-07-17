#!/usr/bin/env python3

"""
Build a corpus for gensim from individual text files.
"""


# == imports ==

import os
import glob
from os.path import join
import re
import pandas as pd
from shutil import copyfile

from gensim import corpora
from gensim import models
import pyLDAvis
import pyLDAvis.gensim
from gensim.models.coherencemodel import CoherenceModel

import datetime
import logging

import warnings
warnings.simplefilter("ignore")

# == general parameters == 

workingdir = join("/", "media", "christof", "mydata", "Dropbox", "5-Lehre", "2019-Sommer/", "Distributional-Semantics-Riga", "")
corpusdir = join(workingdir, "0-datasets", "hkpress", "")
corpusfiles = [join(corpusdir, "hkpress-lemmas.txt")]
stoplistfile = join(corpusdir, "stopwords.txt")
print(stoplistfile)

# == model parameters == 

numtopics = 20
passes = 1000


# == logging and resultsfolder == 

timestamp,ms = datetime.datetime.now().isoformat().split(".")
resultsfolder = join(workingdir, "2-topic-modeling", "hkpress_+" + str(timestamp), "")
if not os.path.exists(resultsfolder): 
    os.makedirs(resultsfolder)

logging.basicConfig(
   filename = join(resultsfolder, "modeling.log"), 
   format='%(asctime)s : %(levelname)s : %(message)s', 
   level=logging.INFO)


# == functions == 

def read_corpusfiles(corpusfiles, stoplistfile): 
    print("read_corpusfiles")
    with open(stoplistfile, "r", encoding="utf8") as infile: 
        stoplist = infile.read().lower().splitlines()
        print("stoplist:", stoplist[0:100], "...")
    listcorpus = []
    for corpusfile in corpusfiles: 
        with open(corpusfile, "r", encoding="utf8") as infile: 
            corpus = infile.read().splitlines()
            onelistcorpus = [[token for token in re.split("\W+", text) if token not in stoplist] for text in corpus]
            listcorpus.extend(onelistcorpus)
    listcorpus = [[token for token in line if token] for line in listcorpus]
    # remove words that appear only once
    print("filter tokens by freq")
    from collections import defaultdict
    frequency = defaultdict(int)
    for line in listcorpus:
        for token in line:
            frequency[token] += 1
    listcorpus = [[token for token in line if frequency[token] > 5] for line in listcorpus]
    with open(join(resultsfolder, "listcorpus.csv"), "a", encoding="utf8") as outfile: 
        for line in listcorpus: 
            line = " ".join(line) + "\n"
            outfile.writelines(line)
    #print(listcorpus)
    return listcorpus


def copy_stoplistfile(stoplistfile, resultsfolder): 
    print("copy_stoplistfile")
    basename = os.path.basename(stoplistfile)
    copyfile(stoplistfile, join(resultsfolder, join(resultsfolder, basename)))


def build_vectorcorpus(listcorpus, resultsfolder): 
    print("build_vectorcorpus")
    dictcorpus = corpora.Dictionary(listcorpus)
    dictcorpus.save(join(resultsfolder, "corpus.dict"))
    vectorcorpus = [dictcorpus.doc2bow(text) for text in listcorpus]
    print("number of types", len(dictcorpus))
    #print(dictcorpus)
    #print(dictcorpus.token2id)
    #print(vectorcorpus)
    return dictcorpus, vectorcorpus


def build_model_multicore(dictcorpus, vectorcorpus, numtopics, passes, workingdir, timestamp): 
    print("build_model_multicore")
    model = models.ldamulticore.LdaMulticore(
        corpus=vectorcorpus,
        id2word=dictcorpus,
        num_topics=numtopics, 
        #random_state=100,
        #update_every=1000,
        #chunksize=100,
        passes=passes,
        workers=3,
        per_word_topics=True)
    model.save(join(resultsfolder, "model.gensim"))
    return model


def build_model_singlecore(dictcorpus, vectorcorpus, numtopics, passes, workingdir, timestamp): 
    print("build_model_singlecore")
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
    model.save(join(resultsfolder, "model.gensim"))
    return model



def get_topics(model, numtopics, resultsfolder): 
    print("get_topics")
    topics = []
    for i in range(0,numtopics): 
        topic = model.show_topic(i, topn=500)
        topic = list(zip(*topic))
        topic = pd.Series(topic[1], index=topic[0], name=str(i))
        topics.append(topic)
    topics = pd.concat(topics, axis=1, keys=[topic.name for topic in topics], sort=False)
    topics = topics.fillna(0)
    with open(join(resultsfolder, "wordprobs.csv"), "w", encoding="utf8") as outfile: 
        topics.to_csv(outfile, sep="\t")


def get_topicwords(model, numtopics, resultsfolder): 
    print("get_topicwords")
    topicdata = model.show_topics(num_topics=numtopics, num_words=1000,formatted=False)
    topicwords = [(tp[0], [wd[0] for wd in tp[1]]) for tp in topicdata]
    topicwordsdict = {}
    for topic,words in topicwords:
        topicwordsdict[str(topic)] = words
    #print(topicwordsdict)
    topicwordsdf = pd.DataFrame.from_dict(topicwordsdict, orient="index")
    print(topicwordsdf.head())
    with open(join(resultsfolder, "topicwords.csv"), "w", encoding="utf8") as outfile: 
        topicwordsdf.to_csv(outfile, sep="\t")
    

def get_doc_topic_matrix(corpus, model, resultsfolder): 
    print("get_doc_topic_matrix")
    document_topics = model.get_document_topics(corpus, per_word_topics=True)
    doc_number = 0
    all_doc_topics = []
    for doc_topics, word_topics, phi_values in document_topics:
        doc_topics = dict(doc_topics)
        doc_topics = pd.Series(doc_topics, name=str(doc_number))
        all_doc_topics.append(doc_topics)
        doc_number +=1
    all_doc_topics = pd.concat(all_doc_topics, axis=1, keys=[s.name for s in all_doc_topics])
    all_doc_topics = all_doc_topics.fillna(0).T
    print(all_doc_topics.head())
    with open(join(resultsfolder, "doc-topic-matrix.csv"), "w", encoding="utf8") as outfile: 
        all_doc_topics.to_csv(outfile, sep="\t")
    

def visualize_model(model, dictcorpus, vectorcorpus, resultsfolder):
    print("visualize_model")
    visualization = pyLDAvis.gensim.prepare(
        model, 
        vectorcorpus, 
        dictcorpus, 
        sort_topics=False)
    pyLDAvis.save_html(visualization, join(resultsfolder, "visualization.html"))


def check_coherence(listcorpus, vectorcorpus, model, numtopics, resultsfolder): 
    print("check_coherence")
    # coherence for the entire model, using several measures
    measures = ["c_v", "c_npmi", "u_mass", "c_uci"]
    coherences = []
    for measure in measures: 
        coherencemodel = CoherenceModel(texts=listcorpus, model=model, corpus=vectorcorpus, coherence=measure, processes=3)
        coherence = coherencemodel.get_coherence()
        coherences.append(coherence)
    coherences = dict(zip(measures, coherences))
    coherences = pd.DataFrame.from_dict(coherences, orient='index', columns=["score"])
    with open(join(resultsfolder, "coherences-model.csv"), "w", encoding="utf8") as outfile: 
        coherences.to_csv(outfile, sep="\t")
    # coherence of each topic, using one measure only
    coherencemodel = CoherenceModel(texts=listcorpus, model=model, corpus=vectorcorpus, coherence="c_v", processes=3)    
    coherences = list(zip(range(0,numtopics), coherencemodel.get_coherence_per_topic()))
    coherences = pd.DataFrame(coherences, columns=["topic", "score"]).sort_values(by="score", ascending=False)
    with open(join(resultsfolder, "coherences-topics.csv"), "w", encoding="utf8") as outfile: 
        coherences.to_csv(outfile, sep="\t")


# == main == 

def main(workingdir, corpusfiles, stoplistfile, resultsfolder, numtopics, passes):
    copy_stoplistfile(stoplistfile, resultsfolder)
    listcorpus = read_corpusfiles(corpusfiles, stoplistfile)
    dictcorpus, vectorcorpus = build_vectorcorpus(listcorpus, resultsfolder)
    model = build_model_singlecore(dictcorpus, vectorcorpus, numtopics, passes, workingdir, resultsfolder)
    #model = build_model_multicore(dictcorpus, vectorcorpus, numtopics, passes, workingdir, resultsfolder)
    #model = models.ldamodel.LdaModel.load(join(workingdir, "gensim", "2018-09-04T08:36:55_192021", "model.gensim"))
    topics = get_topics(model, numtopics, resultsfolder)
    topicwords = get_topicwords(model, numtopics, resultsfolder)
    doc_topic_matrix = get_doc_topic_matrix(vectorcorpus, model, resultsfolder)
    visualize_model(model, dictcorpus, vectorcorpus, resultsfolder)
    check_coherence(listcorpus, vectorcorpus, model, numtopics, resultsfolder)
      
main(workingdir, corpusfiles, stoplistfile, resultsfolder, numtopics, passes)
