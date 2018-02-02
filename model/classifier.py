import numpy as np
import pandas as pd

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

import baseline as base


def concatenate_articles(subset, sid):
    df = pd.DataFrame()

    files = [row[0] for row in subset]
    df["text"] = [open(f).read() for f in files]
    df["file"] = files

    if sid == 0:
        df["label"] = 0
    else:
        df["label"] = 1

    return df


def build_corpus(left, right):
    data_left = concatenate_articles(left, sid=0)
    data_right = concatenate_articles(right, sid=1)

    # combine both corpora
    X = pd.concat([data_left[['text', 'file']], data_right[['text', 'file']]])
    y = pd.concat([data_left['label'], data_right['label']])

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

    text_clf.fit(X_train.text, y_train)
    predicted = text_clf.predict(X_test.text)

    print(metrics.classification_report(y_test, predicted))

    print(metrics.confusion_matrix(y_test, predicted))

    X_test["pred"] = predicted
    results = pd.concat([X_test, y_test], axis=1)

    print(results[results.pred != results.label])
