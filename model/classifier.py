import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

import baseline as base


"""
WORK IN PROGRESS
"""


def build_corpus(subset, sid):
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


def test_unseen(data_path, cvec, tft, clf, y_train):
    article_list = []
    files = os.listdir(data_path)

    for art_file in files:
        with open("/".join([data_path, art_file])) as f:
            article = " ".join(x.strip('\n') for x in f.readlines())
            article_list.append(article)

    X_new_counts = cvec.transform(article_list)
    X_new_tfidf = tft.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)

    for doc, category in zip(article_list, predicted):
        print('{} => {}'.format(doc, y_train[category]))


if __name__ == "__main__":
    # Parse the data sets for left- and right-wing
    left_wing_train = base.read_csv('../data/train/left_wing_train.csv')
    right_wing_train = base.read_csv('../data/train/right_wing_train.csv')

    X_left, y_left = build_corpus(left_wing_train, sid=0)
    X_right, y_right = build_corpus(right_wing_train, sid=1)

    # combine both corpora
    X_train = X_left + X_right
    y_train = np.append(y_left, y_right)

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    print("X_train: {}".format(X_train_counts.shape))
    print("y_train: {}".format(y_train.shape))

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    nb_clf = MultinomialNB().fit(X_train_tfidf, y_train)

    test_unseen('../data/pi-news/pi_texts', count_vect, tfidf_transformer, nb_clf, y_train)
