import numpy as np
import pandas as pd

from sklearn import metrics
from sklearn import tree
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.utils import shuffle

import baseline as base
import named_entities as ne

def concatenate_articles(subset, named_entities, sid):
    df = pd.DataFrame()

    files = [row[0] for row in subset]
    articles = [open(f).read() for f in files]   
    
    
    merkellist = []
    entities_list = []
    for art in articles:
        merkelcounter = 0
        for word in art.split():
            if word == "Merkel":
                merkelcounter += 1
        merkellist.append(merkelcounter)

        curr_entities = ne.extract_named_entities(named_entities, art)
        entities_list.append(curr_entities)
        

    #print(len(entities_list))
    df['angela'] = merkellist

    df['named_entities'] = entities_list
    print(df['named_entities'])
    #print(df['named_entities'].shape)
    df['text'] = articles

    df['file'] = files

    if sid == 0:
        df['label'] = 0
    else:
        df['label'] = 1

    return df


def build_corpus(left, right):
    ne_left = most_common_entities(left)
    ne_right = most_common_entities(right)
    
    data_left = concatenate_articles(left, ne_left, sid=0)
    data_right = concatenate_articles(right, ne_right, sid=1)

    # Combine both corpora and shuffle it
    data = pd.concat([data_left, data_right])
    shuffled_data = shuffle(data).reset_index(drop=True)

    X = shuffled_data[['text', 'file', 'angela', 'named_entities']]
    y = shuffled_data['label']

    return X, y


def most_common_entities(subset):
    files = [row[0] for row in subset]
    articles = [open(f).read() for f in files]   

    entities_dict = dict()
    for art in articles:
        entities_dict = ne.add_entities(entities_dict, art)
    most_common = ne.get_most_common(entities_dict, number=200)

    return most_common

if __name__ == "__main__":
    np.random.seed(10)

    # Parse the datasets
    #left_wing_train = base.read_csv('../data/train/left_wing_train.csv')
    #right_wing_train = base.read_csv('../data/train/right_wing_train.csv')

    #left_wing_test = base.read_csv('../data/test/left_wing_test.csv')
    #right_wing_test = base.read_csv('../data/test/right_wing_test.csv')
    left_wing_train = base.read_csv('../data/train/left_wing_train_short.csv')
    right_wing_train = base.read_csv('../data/train/right_wing_train_short.csv')

    left_wing_test = base.read_csv('../data/test/left_wing_test_short.csv')
    right_wing_test = base.read_csv('../data/test/right_wing_test_short.csv')

    X_train, y_train = build_corpus(left_wing_train, right_wing_train)
    X_test, y_test = build_corpus(left_wing_test, right_wing_test)

    # Training
    """
    text_clf = Pipeline([('vect', TfidfVectorizer(max_features=100)),
                         #('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB())])
    text_clf.fit(X_train.text, y_train)
    # Apply trained model on test set
    predicted = text_clf.predict(X_test.text)
    """

    text_clf = tree.DecisionTreeClassifier()
    text_clf.fit(X_train.named_entities.reshape((X_train.named_entities.shape[0], 1)), y_train)
    predicted = text_clf.predict(X_test.angela.reshape((X_test.named_entities.shape[0], 1)))

    # Evaluation
    print(metrics.accuracy_score(y_test, predicted))
    print(metrics.classification_report(y_test, predicted))
    print(metrics.confusion_matrix(y_test, predicted))

    X_test["pred"] = predicted
    results = pd.concat([X_test, y_test], axis=1)

    # Print wrong predictions
    print(results[results.pred != results.label])
