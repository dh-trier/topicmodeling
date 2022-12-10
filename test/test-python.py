"""
============================
Test your installation
============================

This is a script for testing whether Python has been properly installed with all required libraries. See the separate instructions file for details. 

"""



#== Initial test. 

print("\n=== Testing that the script runs. ===")
print("That's a good start! You have just run this Python script!\n")


print("\n=== Finding out which version of Python you have. ===")
import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
    print("This script requires Python 3.6 or higher!")
    sys.exit(1)
print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))



#== Checking the libraries are installed and can be imported.  

try:
    import pandas as pd
    print("OK. Looks like pandas is installed. Great!")
except:
    print("ERROR! Looks like the library pandas is missing. Please install it!")
    print("The easiest way to do this is to use \"pip3 install pandas\" on the command line.")

try:
    import gensim
    print("OK. Looks like gensim is installed. Great!")
except:
    print("ERROR! Looks like the library gensim is missing. Please install it!")
    print("The easiest way to do this is to use \"pip3 install gensim\" on the command line.")


try:
    import numpy
    print("OK. Looks like numpy is installed. Great!")
except:
    print("ERROR! Looks like the library numpy is missing. Please install it!")
    print("The easiest way to do this is to use \"pip3 install numpy\" on the command line.")

try:
    import pyLDAvis
    print("OK. Looks like pyLDAvis is installed. Great!")
except:
    print("ERROR! Looks like the library pyLDAvis is missing. Please install it!")
    print("The easiest way to do this is to use \"pip3 install pyLDAvis\" on the command line.")

try: 
    import nltk
    from nltk.stem import WordNetLemmatizer
    print("OK. Looks like NLTK is installed. Great!")
except:
    print("ERROR! Looks like the library NLTK is missing. Please install it!")
    print("The easiest way to do this is to use \"pip3 install nltk\" on the command line.")


try: 
    from textblob import TextBlob
    print("OK. Looks like textblob is installed. Great!")
except:
    print("ERROR! Looks like the library textblob is missing. Please install it!")
    print("The easiest way to do this is to use \"pip3 install textblob\" on the command line.")

try: 
    import seaborn
    print("OK. Looks like seaborn is installed. Great!")
except:
    print("ERROR! Looks like the library seaborn is missing. Please install it!")
    print("The easiest way to do this is to use \"pip3 install seaborn\" on the command line.")

try: 
    import wordcloud
    print("OK. Looks like wordcloud is installed. Great!")
except:
    print("ERROR! Looks like the library wordcloud is missing. Please install it!")
    print("The easiest way to do this is to use \"pip3 install wordcloud\" on the command line.")


try: 
    import sklearn
    print("OK. Looks like sklearn is installed. Great!")
except:
    print("ERROR! Looks like the library sklearn is missing. Please install it!")
    print("The easiest way to do this is to use \"pip3 install sklearn\" on the command line.")



#== Downloading some model file for NLTK

print("\n=== Testing that model files for NLTK are downloaded correctly. ===")
try: 
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    print("OK. Looks like all required NLTK models have been downloaded. Great!")
except:
    print("ERROR! There seems to be a problem with downloading NLTK model files. Please check!")
   

#== Actually testing pandas

print("\n=== Testing that pandas works. ===")
import os
from os.path import join
workdir = join(os.path.realpath(os.path.dirname(__file__)))
try: 
    with open(join(workdir, "test-metadata.csv"), "r", encoding="utf8") as infile:
        metadata = pd.read_csv(infile, sep=",")
        #print(metadata.head(3))
        print("OK. Looks like the metadata file can be read using pandas. Great!")
except:
    print("ERROR! Looks like there is an issue either with finding the metadata file or with using the pandas library. Please check!")



#== Actually testing gensim

print("\n=== Testing that gensim works. ===")
try: 
    from gensim.models.ldamodel import LdaModel
    from gensim.test.utils import common_corpus
    print("OK. Looks like the gensim modules can be imported correctly.")
except:
    print("ERROR! There is an issue with the gensim installation. Please check!")

try:
    mymodel = LdaModel(common_corpus, num_topics=10)
    print("OK. Looks like the gensim model was loaded correctly.")
except:
    print("ERROR! The gensim model file could not be loaded.")
                       



#== Testing textblob installation
    
print("\n=== Testing that textblob actually works, using the following sentence. ===")
text = "The trees in front of these houses are looking more green than in previous years."
print("\""+text+"\"")
try:
    blob = TextBlob(text)
    tokens = blob.words
    print(tokens)
    print("OK. What is shown in the line above should be the separate words from the above sentence, like this: [\'The\', \'trees\', \'in\'....]")
except:
    print("ERROR! Tokenization with the textblob library has failed.")    
    print("What is shown in the line above should be the separate words from the above sentence, like this: [\'The\', \'trees\', \'in\'....]")
try:
    blob = TextBlob(text)
    tagged = blob.tags
    nouns = [item[0] for item in tagged if "NN" in item[1]]
    print(nouns)
    print("OK. The line above this one should have a list of nouns, like this: [\'trees\', \'front\', \'houses\', \'years\'].")
except:
    print("ERROR! POS-Tagging and selection of nouns has failed.")    
    print("The line above this one should have a list of nouns, like this: [\'trees\', \'front\', \'houses\', \'years\'].")

