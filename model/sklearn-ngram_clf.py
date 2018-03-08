import pandas as pd
import argparse

from sklearn import metrics
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils import shuffle

import baseline as base
from features import sentiment, named_entities, ngrams, quoted, artlen, sentlen, pos_tags

#add command line arguments
argParser = argparse.ArgumentParser(description="Train and test a political classifier for texts")
#choose features to use
argParser.add_argument('-f', nargs='*', choices=["ngrams", "named_ents", "sentiment", "artlen", "sentlen", "POS", "quoted"])
#choose number of named entities to use
argParser.add_argument('-n', default=200)
#decide, whether to use short corpus
argParser.add_argument('-s', choices=['yes','no','y','n'])
#decide, whether to use test set from outlets unseen in training
argParser.add_argument('-u', choices=['yes','no','y','n'])
#set number of unigrams
argParser.add_argument('-1', default=10000)
#set number of bigrams
argParser.add_argument('-2', default=2000)


def build_subset(subset, sid, split):
    # Create DataFrame
    df = pd.DataFrame()

    # Read all files of a subset
    files = [row[0] for row in subset]
    articles = [open(f).read() for f in files]

    # Fill DataFrame with columns
    df['text'] = articles
    df['file'] = files
    df['label'] = sid
    df['split'] = split

    return df


def build_corpus(train_L, train_R, test_L, test_R):
    # Create a DataFrame for each subset
    train_L = build_subset(train_L, sid="0", split="train")
    train_R = build_subset(train_R, sid="1", split="train")
    test_L = build_subset(test_L, sid="0", split="test")
    test_R = build_subset(test_R, sid="1", split="test")

    # Combine all subsets and shuffle the resulting DataFrame
    data = pd.concat([train_L, train_R, test_L, test_R])
    data = shuffle(data).reset_index(drop=True)

    return data


def split_X_and_y(data):
    # Split the label column from the rest
    X = data.drop(['label'], axis=1)
    y = data['label']
    return X, y


def train(data, clf):
    print("Features: n-grams (sklearn)")

    # Untangle data
    train_data = data[data['split'] == "train"]
    test_data = data[data['split'] == "test"]

    X_train, y_train = split_X_and_y(train_data)
    X_test, y_test = split_X_and_y(test_data)

    # Unselect features from X
    X_train = X_train.drop(['file', 'split'], axis=1).fillna(0)
    X_test = X_test.drop(['file', 'split'], axis=1).fillna(0)

    # sklearn n-gram feature
    text_clf = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2))),
                         ('clf', clf)])

    # Training
    text_clf.fit(X_train.text, y_train)

    # Apply trained model on test set
    predicted = text_clf.predict(X_test.text)

    # Evaluation
    print(metrics.classification_report(y_test, predicted))
    print(metrics.confusion_matrix(y_test, predicted))
    print("\n Accuracy: {} \n".format(metrics.accuracy_score(y_test, predicted)))

    X_test["pred"] = predicted
    results = pd.concat([X_test, y_test], axis=1)

    # Print wrong predictions
    print(results[results.pred != results.label])


if __name__ == "__main__":
    # Argument parsing
    args = vars(argParser.parse_args())
    if args['s'] is None or args['s'] == 'no' or args['s'] == 'n':
        small_dataset = False
    else:
        small_dataset = True

    use_ngrams = False
    use_named_ents = False
    use_sentiment = False
    use_artlen = False
    use_sentlen = False
    use_POS = False
    use_quoted = False

    # Feature selection
    if args['f'] is not None:
        if "ngrams" in args['f']:
            use_ngrams = True
        if "named_ents" in args['f']:
            use_named_ents = True
        if "sentiment" in args['f']:
            use_sentiment = True
        if "artlen" in args['f']:
            use_artlen = True
        if "sentlen" in args['f']:
            use_sentlen = True
        if "POS" in args['f']:
            use_POS = True
        if "quoted" in args['f']:
            use_quoted = True

    # Select test set
    if args['u'] is None or args['u'] == 'yes' or args['u'] == 'y':
        unseen = True
    else:
        unseen = False

    ne_number = int(args['n'])

    uni_number = int(args['1'])
    bi_number = int(args['2'])

    # Parse the datasets

    if small_dataset:
        left_wing_train = base.read_csv('../data/train/left_wing_train_short.csv')
        right_wing_train = base.read_csv('../data/train/right_wing_train_short.csv')
        left_wing_test = base.read_csv('../data/test/left_wing_test_short.csv')
        right_wing_test = base.read_csv('../data/test/right_wing_test_short.csv')
    else:
        left_wing_train = base.read_csv('../data/train/left_wing_train.csv')
        right_wing_train = base.read_csv('../data/train/right_wing_train.csv')
        if unseen:
            left_wing_test = base.read_csv('../data/test/true_left_wing_test.csv')
            right_wing_test = base.read_csv('../data/test/true_right_wing_test.csv')
        else:
            left_wing_test = base.read_csv('../data/test/left_wing_test.csv')
            right_wing_test = base.read_csv('../data/test/right_wing_test.csv')
            

    data = build_corpus(left_wing_train, right_wing_train,
                        left_wing_test, right_wing_test)

    # Add features based on arguments
    if use_POS:
        data = pos_tags.add_feature(df=data)  # POS tag feature
    if use_named_ents:
        data = named_entities.add_feature(data, ne_number)
    if use_sentiment:
        data = sentiment.add_feature(data)
    if use_artlen:
        data = artlen.add_feature(data)
    if use_sentlen:
        data = sentlen.add_feature(data)
    if use_quoted:
        data = quoted.add_feature(data)
    if use_ngrams:
        data = ngrams.add_feature(data, uni_number, bi_number)
    
    # Select classifier and train
    clf = SGDClassifier() #tree.DecisionTreeClassifier()
    train(data, clf)
