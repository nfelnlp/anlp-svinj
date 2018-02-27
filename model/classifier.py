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

def concatenate_articles(left, right, named_entities):
    df_left = pd.DataFrame()
    df_right = pd.DataFrame()

    files_left = [row[0] for row in left]
    articles_left = [open(f).read() for f in files_left]   

    files_right = [row[0] for row in right]
    articles_right = [open(f).read() for f in files_right]   

    
    entities_left = []
    entities_right = []
    for left_art, right_art in zip(articles_left, articles_right):

        curr_entities_left = ne.extract_named_entities(named_entities, left_art)
        entities_left.append(curr_entities_left)
        
        curr_entities_right = ne.extract_named_entities(named_entities, right_art)
        entities_right.append(curr_entities_right)


    
    ne_features_left = pd.DataFrame(entities_left)
    df_left = pd.concat([df_left, ne_features_left], axis=1)

    ne_features_right = pd.DataFrame(entities_right)
    df_right = pd.concat([df_right, ne_features_right], axis=1)

    df_left['text'] = articles_left
    df_right['text'] = articles_right




    df_left['file'] = files_left
    df_right['file'] = files_right

    df_left['label'] = 0
    df_right['label'] = 1

    return df_left, df_right


def build_corpus(left_train, right_train, left_test, right_test, most_common_ne):

    ## Prepare training data

    data_left, data_right = concatenate_articles(left_train, right_train, most_common_ne)
    
    #data_left = concatenate_articles(left, most_common_ne, sid=0)
    #data_right = concatenate_articles(right, most_common_ne, sid=1)

    # Combine both corpora and shuffle it
    data = pd.concat([data_left, data_right])
    shuffled_data = shuffle(data).reset_index(drop=True)

    #X = shuffled_data[['text', 'file', 'angela', 'named_entities']]
    X_train = shuffled_data.drop(['label'], axis=1)
    y_train = shuffled_data['label']



    ## Prepare test data

    data_left, data_right = concatenate_articles(left_test, right_test, most_common_ne)
    
    # Combine both corpora and shuffle it
    data = pd.concat([data_left, data_right])
    shuffled_data = shuffle(data).reset_index(drop=True)

    #X = shuffled_data[['text', 'file', 'angela', 'named_entities']]
    X_test = shuffled_data.drop(['label'], axis=1)
    y_test = shuffled_data['label']


    return X_train, y_train, X_test, y_test


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

    most_common_ne = most_common_entities(left_wing_train + right_wing_train)
    
    #X_train, y_train = build_corpus(left_wing_train, right_wing_train, most_common_ne)
    #X_test, y_test = build_corpus(left_wing_test, right_wing_test, most_common_ne)

    X_train, y_train, X_test, y_test = build_corpus(
        left_wing_train, right_wing_train, left_wing_test, right_wing_test, most_common_ne)
    
    """
    text_clf = Pipeline([('vect', TfidfVectorizer(max_features=100)),
    #                     #('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB())])
    text_clf.fit(X_train, y_train)
    # Apply trained model on test set
    predicted = text_clf.predict(X_test.text)
    """

    # Select features from X_train

    X_train = X_train.drop(['text', 'file'], axis=1).fillna(0)
    X_test = X_test.drop(['text', 'file'], axis=1).fillna(0)

    # Training
    text_clf = tree.DecisionTreeClassifier()
    text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_test)

    # Evaluation
    print(metrics.accuracy_score(y_test, predicted))
    print(metrics.classification_report(y_test, predicted))
    print(metrics.confusion_matrix(y_test, predicted))

    X_test["pred"] = predicted
    results = pd.concat([X_test, y_test], axis=1)

    # Print wrong predictions
    print(results[results.pred != results.label])

    print("Hallo")

    #print correct predictions
    print(results[results.pred == results.label])
    
