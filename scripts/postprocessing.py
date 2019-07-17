"""
Topic Modeling with gensim: postprocessing.
"""

from os.path import join
import pandas as pd
import helpers



def get_topics(model, numtopics, resultsfolder): 
    topics = []
    for i in range(0,numtopics): 
        topic = model.show_topic(i, topn=50)
        topic = list(zip(*topic))
        topic = pd.Series(topic[1], index=topic[0], name=str(i))
        topics.append(topic)
    topics = pd.concat(topics, axis=1, keys=[topic.name for topic in topics], sort=False)
    topics = topics.fillna(0)
    with open(join(resultsfolder, "wordprobs.csv"), "w", encoding="utf8") as outfile: 
        topics.to_csv(outfile, sep="\t")


def get_topicwords(model, numtopics, resultsfolder): 
    topicdata = model.show_topics(num_topics=numtopics, num_words=100,formatted=False)
    topicwords = [(tp[0], [wd[0] for wd in tp[1]]) for tp in topicdata]
    topicwordsdict = {}
    for topic,words in topicwords:
        topicwordsdict[str(topic)] = words
    topicwordsdf = pd.DataFrame.from_dict(topicwordsdict, orient="index").T
    with open(join(resultsfolder, "topicwords.csv"), "w", encoding="utf8") as outfile: 
        topicwordsdf.to_csv(outfile, sep="\t")
    

#def get_doc_topic_matrix(corpus, model, resultsfolder): 
#    print("get_doc_topic_matrix")
#    document_topics = model.get_document_topics(corpus, per_word_topics=True)
#    doc_number = 0
#    all_doc_topics = []
#    for doc_topics, word_topics, phi_values in document_topics:
#        doc_topics = dict(doc_topics)
#        doc_topics = pd.Series(doc_topics, name=str(doc_number))
#        all_doc_topics.append(doc_topics)
#        doc_number +=1
#    all_doc_topics = pd.concat(all_doc_topics, axis=1, keys=[s.name for s in all_doc_topics])
#    all_doc_topics = all_doc_topics.fillna(0).T
#    #print(all_doc_topics.head())
#    with open(join(resultsfolder, "doc-topic-matrix.csv"), "w", encoding="utf8") as outfile: 
#        all_doc_topics.to_csv(outfile, sep="\t")


def main(workdir, identifier, numtopics):
    print("\n== postprocessing ==")
    model = helpers.load_model(workdir, identifier)
    resultsfolder = join(workdir, "results", identifier)
    get_topics(model, numtopics, resultsfolder)
    get_topicwords(model, numtopics, resultsfolder)
    print("done postprocessing")
