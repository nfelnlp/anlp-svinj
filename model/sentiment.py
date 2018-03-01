import nltk
import polyglot
from polyglot.text import Text
import collections as col

#extracts the polarity from article
def polarity(article):
    try:
        words = Text(article).words
    except:
        #This is neccessary because polyglot has problems with some UTF-8 characters
        printable = ''.join(x for x in article if x.isprintable())
        words = Text(printable).words

    # polarity for negative=-1, for positive=1, for neutral=0 so summing up gives the overall polarity
    polarity = 0
    for w in words:
        polarity += w.polarity

    return polarity
