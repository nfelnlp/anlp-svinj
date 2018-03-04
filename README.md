# Political text classification (ANLP group project 2017/18)

A classifier for radically right- and left-wing texts.

## Classifier

The main file is model/default_clf.py. In order to run it, navigate to the model directory.

default_clf.py will first train a classifier based on a training corpus and then test the classifier.

There are a number of command line options for default_clf.py:
* -f ... choose which features to use
  * ngrams: most common uni- and bigrams
  * named_ents: most common named entities
  * sentiment: sentiment analysis
  * artlen: article length
  * sentlen: sentence length
  * POS: (raw counts of) parts of speech
  * quoted: percentage of quoted speech
* -n ... set number of named entities to use (default: 200)
* -s ... decide whether to use a short training and test corpus (for debugging purposes)
* -u ... set which test corpus to use
  * y, yes ... use outlets from which there weren't any articles in the training corpus
  * n, no ... use outlets from which there were articles in the training corpus
* -1 ... set number of unigrams to use (default: 10000)
* -2 ... set number of bigrams to use (default: 2000)

The type of the classifier is Decision Tree (hard-coded), since it performed far better than all our comparisons (Naive Bayes, Linear SVM, Random Forest).


### Test on a single input file

In addition, there is model/test_single_article.py which works almost exactly like default_clf.py.
However, since there is not distinction between test corpora, it does not have the -u flag.
Instead, it needs an additional -test flag to be filled with the path to a text file (article).

Example usage:
```
python3 test_single_article.py -f ngrams sentiment -test ../data/deutsche-stimme/articles/0054_Der-Terror-ist-in-Deutschland-.txt
```


## Dependencies

The classifier itself works with [pandas](https://pandas.pydata.org/), [sklearn](http://scikit-learn.org/stable/index.html) and [NLTK](http://www.nltk.org/).

As outlined above, there are seven implemented features. Some of them require additional Python packages:
* [polyglot](http://polyglot.readthedocs.io/en/latest/index.html)
* [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) + [treetaggerwrapper](http://treetaggerwrapper.readthedocs.io/en/latest/#)
