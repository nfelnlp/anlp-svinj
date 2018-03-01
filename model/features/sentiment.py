import nltk
import polyglot
from polyglot.text import Text
import collections as col

import pandas as pd


def add_feature(df):
    # Retrieve text data from dataframe
    articles = df["text"].tolist()

    # Add new column for polarity values to dataframe
    df["sentiment"] = pd.Series(polarity(articles))

    return df


# Extracts the polarity from articles
def polarity(articles):
    polarities = []
    for art in articles:
        try:
            words = Text(art).words
        except:
            #This is neccessary because polyglot has problems with some UTF-8 characters
            printable = ''.join(x for x in art if x.isprintable())
            words = Text(printable).words

        # polarity for negative=-1, for positive=1, for neutral=0 so summing up gives the overall polarity
        polarity = 0
        for w in words:
            polarity += w.polarity

        polarities.append(polarity)
    return polarities
