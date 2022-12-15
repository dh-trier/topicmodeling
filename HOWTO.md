## Welcome to the Python-based topic modeling pipeline

This set of Python scripts has been developed for teaching purposes. Its fundamental aim is to provide a minimal, working implementation of a Python-based processing pipeline for Topic Modeling. 

These scripts are meant as complementary to a slide-deck that explains Topic Modeling to an audience of scholars from the (Digital) Humanities. See here: https://christofs.github.io/riga/#/.  

## Requirements 

You will need a computer on which you can install and run Python. Most modern laptops running a reasonably recent version of Windows, Mac OS or Linux (e.g. Ubuntu 18.04+) should be just fine, but smaller devices like tablets running Android or iOS won't be enough. 

Please install the following: 

* Python 3: Please use Python 3.6 or higher. The scripts will not work with Python 2. 
* Python3 pip for installation of further libraries. 
* A Python IDE of your choice, for example Thonny, Geany, Spyder or PyCharm.
* Some additional libraries in their most recent version (with their respective dependencies): 
    * "numpy", see: https://www.numpy.org/
    * "pandas", see: https://pandas.pydata.org/
    * "nltk", see: https://www.nltk.org/
    * "textblob", see: https://textblob.readthedocs.io/en/dev/
    * "gensim", see: https://radimrehurek.com/gensim/install.html
    * "pyLDAvis", see: https://github.com/bmabey/pyLDAvis
    * "seaborn", see: https://seaborn.pydata.org/
    * "sklearn", see: https://scikit-learn.org/stable/
    * "wordcloud", see: https://github.com/amueller/word_cloud
    * To work with French and/or German texts: textblob_fr and/or textblob_de

## Installation

Once you have installed the above-mentioned software and Python libaries, it is sufficient to download or clone this Github repository. You can then run the scripts and access the sample dataset. 

## Testing your installation 

Before trying to use the scripts, you should test your installation. For this test, please follow the instructions provided here in the folder called "test". 

## Usage notes 

* For simplicity's sake, this pipeline relies on TextBlob for linguistic annotations. This is an interface to NLTK and provides annotation resources for English, French and German. If you want to work with a different language, you need to supply the annotation step yourself, basically plugging in an alternative to the module called "preprocessing.py". 
* The pipeline assumes your corpus is available in the shape of plain text files encoded in UTF-8 with each document being in its own file. The filename is the text's identifier. 
* The "make_heatmap.py" visualization requires a metadata file called "metadata.csv" to be present, in the form of a CSV file. You need to adjust the variable "cats" in "run_pipeline.py" and possibly make minor adjustments in the "make_heatmap.py" script to account for the metadata categories that are present in your metadata file. 
* If you want to use your own datasets, simply add a folder in the "datasets" directory and replicate the folder structure of the example datasets. 

## Licence 

This software is distributed under a so-called "unlicence", that is, with no restrictions or conditions on re-use, re-distribution, modification. However, it also comes with no warranty whatsoever. See: https://choosealicense.com/licenses/unlicense/

## Maintainer and contact

This code has been put together by Christof Schöch, University of Trier, Germany, in July 2019. In case you have suggestions for improvement or run into problems, please use the Github issue tracker. Last (minor) update December 14, 2022. 
