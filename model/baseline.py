import sys
import csv
import os
import re
import nltk
from util import *
from datetime import datetime
from datetime import date
#from nltk.metrics import BigramAssocMeasures
from nltk.tokenize import word_tokenize
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import BigramAssocMeasures

# Change the date in order to get more balance between left- and rightwing data 
# since there is a lot of old data in the rightwing dataset.
IGNORE_BEFORE_DATE = datetime.strptime("2007-01-01", "%Y-%m-%d")

# When calculating uni- and bigram frequencies, the words have to apper at least MIN_FREQ-times
MIN_FREQ = 10

# Savely parse string to date
def get_date(string):
    try:
        return datetime.strptime(string, "%Y-%m-%d") 
    except:
        return datetime.date(1970, 1, 1)


# Parses a csv file and calculates the paths relative to the location of this script
# Returns a list of rows containint out of the triples (PATH, URL, DATE)
def read_csv(path):
    rows = []
    print('Reading:', path)
    rel = '/'.join(path.split('/')[:-1])
    row_cnt = 0
    with open(path, 'r') as inf:
       reader = csv.reader(inf, delimiter=' ', quotechar='|')
       for row in reader:
            row[0] = rel + '/' + row[0]
            date = get_date(row[2]) 
            if os.path.isfile(row[0]):
                if date >= IGNORE_BEFORE_DATE:
                    rows.append((row[0], row[1], date))
                    row_cnt += 1
    print(row_cnt, 'rows read\n')
    return rows

# Reads the text file of every row, tokenizes it and returns a list with all tokenize texts
def merge_to_corpus(rows, prefix):
    corpus = [] 
    l = len(rows)
    token_cnt = 0
    printProgressBar(0, l, prefix = prefix, suffix = 'Complete', length = 50)
    for i, row in enumerate(rows):
        with open(row[0]) as f:
            content = [x.strip('\n') for x in f.readlines()]
            tokens = word_tokenize("\n".join(content))
            token_cnt += len(tokens)
            corpus.append(tokens)
            # Update Progress Bar
            printProgressBar(i + 1, l, prefix = prefix, suffix = 'Complete', length = 50)
    print(token_cnt, 'tokens read\n')
    return corpus


# Entry Point
if __name__ == "__main__":
    # Parse the data sets for left- and right-wing
    left_wing_train = read_csv('../data/train/left_wing_train.csv')
    right_wing_train = read_csv('../data/train/right_wing_train.csv')
    
    left_wing_corpus = merge_to_corpus(left_wing_train, 'Tokenizing left-wing:')
    right_wing_corpus = merge_to_corpus(right_wing_train, 'Tokenizing right-wing:')

    # Ignoring too common or unwanted words
    ignored_words = nltk.corpus.stopwords.words('german')
    ignored_words.extend(["junge", "freiheit", "www.jungefreiheit.de", "co."])

    # Filter bigrams, ignored words and words that are too small are ignored
    bigram_measures = BigramAssocMeasures() 
    word_filter = lambda w: len(w) < 3 or w.lower() in ignored_words

    # Calculate most common bigrams
    print("\nCalculating left-wing bigrams")
    left_finder = BigramCollocationFinder.from_documents(left_wing_corpus)
    left_finder.apply_freq_filter(MIN_FREQ)
    left_finder.apply_word_filter(word_filter)
    print(left_finder.nbest(bigram_measures.likelihood_ratio, 10), '\n')

    print("Calculating right-wing bigrams")
    right_finder = BigramCollocationFinder.from_documents(right_wing_corpus)
    right_finder.apply_freq_filter(MIN_FREQ)
    right_finder.apply_word_filter(word_filter)
    print(right_finder.nbest(bigram_measures.likelihood_ratio, 10), '\n')

    # Calculate most common unigrams
    print("Calculating left-wing unigrams")
    left_wing_tokens = [item for sublist in left_wing_corpus for item in sublist]
    left_wing_fdist = nltk.FreqDist(left_wing_tokens)
    print(left_wing_fdist.most_common()[:10], '\n')

    print("Calculating right-wing unigrams")
    right_wing_tokens = [item for sublist in right_wing_corpus for item in sublist]
    right_wing_fdist = nltk.FreqDist(right_wing_tokens)
    print(right_wing_fdist.most_common()[:10], '\n')
