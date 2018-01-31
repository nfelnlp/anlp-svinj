import os
import numpy as np

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import baseline as base


def concatenate_articles(subset, sid):
    subcorpus = []

    for i, row in enumerate(subset):
        with open(row[0]) as f:
            # concatenate all sentences to one string
            article = " ".join(x.strip('\n') for x in f.readlines())
            subcorpus.append(article)

    # add labels
    if sid == 0:
        labels = np.zeros((len(subcorpus), 1), dtype=np.int)
    else:
        labels = np.ones((len(subcorpus), 1), dtype=np.int)

    return subcorpus, labels


def build_corpus(left, right):
    X_left, y_left = concatenate_articles(left, sid=0)
    X_right, y_right = concatenate_articles(right, sid=1)

    # combine both corpora
    X = X_left + X_right
    y = np.append(y_left, y_right)

    return X, y


if __name__ == "__main__":
    # Parse the datasets
    left_wing_train = base.read_csv('../data/train/left_wing_train.csv')
    right_wing_train = base.read_csv('../data/train/right_wing_train.csv')

    left_wing_test = base.read_csv('../data/test/left_wing_test.csv')
    right_wing_test = base.read_csv('../data/test/right_wing_test.csv')

    X_train, y_train = build_corpus(left_wing_train, right_wing_train)
    X_test, y_test = build_corpus(left_wing_test, right_wing_test)

    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', SGDClassifier())])

    text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_test)

    print(metrics.classification_report(y_test, predicted))

    print(metrics.confusion_matrix(y_test, predicted))
