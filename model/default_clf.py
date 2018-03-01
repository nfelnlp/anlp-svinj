import pandas as pd

from sklearn import metrics
from sklearn import tree
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils import shuffle

import baseline as base

#from features import pos_tags, sentiment
from features import sentiment

def build_subset(subset, sid, split):
    # Read all files of a subset
    df = pd.DataFrame()
    files = [row[0] for row in subset]
    articles = [open(f).read() for f in files]

    df['text'] = articles
    df['file'] = files
    df['label'] = sid
    df['split'] = split

    return df


def build_corpus(train_L, train_R, test_L, test_R):
    train_L = build_subset(train_L, sid="0", split="train")
    train_R = build_subset(train_R, sid="1", split="train")
    test_L = build_subset(test_L, sid="0", split="test")
    test_R = build_subset(test_R, sid="1", split="test")

    # Combine all corpora and shuffle it
    data = pd.concat([train_L, train_R, test_L, test_R])
    data = shuffle(data).reset_index(drop=True)

    return data


def split_X_and_y(data):
    X = data.drop(['label'], axis=1)
    y = data['label']
    return X, y


def train(data, clf):
    # Untangle data
    train_data = data[data['split'] == "train"]
    test_data = data[data['split'] == "test"]

    X_train, y_train = split_X_and_y(train_data)
    X_test, y_test = split_X_and_y(test_data)

    # Unselect features from X
    X_train = X_train.drop(['text', 'file', 'split'], axis=1).fillna(0)
    X_test = X_test.drop(['text', 'file', 'split'], axis=1).fillna(0)

    # Training
    clf.fit(X_train, y_train)

    # Apply trained model on test set
    predicted = clf.predict(X_test)

    # Evaluation
    print(metrics.classification_report(y_test, predicted))
    print(metrics.confusion_matrix(y_test, predicted))
    print("\n Accuracy: {} \n".format(metrics.accuracy_score(y_test, predicted)))

    X_test["pred"] = predicted
    results = pd.concat([X_test, y_test], axis=1)

    # Print wrong predictions
    print(results[results.pred != results.label])


if __name__ == "__main__":
    # Parse the datasets
    small_dataset = True

    if small_dataset:
        left_wing_train = base.read_csv('../data/train/left_wing_train_short.csv')
        right_wing_train = base.read_csv('../data/train/right_wing_train_short.csv')
        left_wing_test = base.read_csv('../data/test/left_wing_test_short.csv')
        right_wing_test = base.read_csv('../data/test/right_wing_test_short.csv')
    else:
        left_wing_train = base.read_csv('../data/train/left_wing_train.csv')
        right_wing_train = base.read_csv('../data/train/right_wing_train.csv')
        left_wing_test = base.read_csv('../data/test/true_left_wing_test.csv')
        right_wing_test = base.read_csv('../data/test/true_right_wing_test.csv')

    data = build_corpus(left_wing_train, right_wing_train,
                        left_wing_test, right_wing_test)

    # Add features
    #data = pos_tags.add_features(df=data)  # POS tag feature
    data = sentiment.add_feature(data)

    # Select classifier and train
    clf = tree.DecisionTreeClassifier()
    train(data, clf=clf)
