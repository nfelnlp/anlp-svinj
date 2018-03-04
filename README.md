# Political text classification

## ANLP group project 2017/18

A classifier for radically right- and left-wing texts.

The main file is model/default_clf.py. In order to run it, navigate to the model directory.

default_clf.py will first train a classifier based on a training corpus and then test the classifier.

There are a number of command line options for default_clf.py:
* -f ... choose which features to use
  * ngrams: most common uni- and bigrams
  * named_ents: most common named entities
  * sentiment: sentiment analysis
  * artlen: article length
  * sentlen: sentence length
  * POS: parts of speech
  * quoted: percentage of quoted speech
* -n ... set number of named entities to use (default: 200)
* -s ... decide, whether to use a short training and test corpus (for debugging purposes)
* -u ... set, which test corpus to use
  * y, yes ... use outlets from which there weren't any articles in the training corpus
  * n, no ... use outlets from which there were articles in the training corpus
* -1 ... set number of unigrams to use (default: 10000)
* -2 ... set number of bigrams to use (default: 2000)