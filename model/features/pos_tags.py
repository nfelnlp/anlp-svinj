import pandas as pd
import treetaggerwrapper

from collections import defaultdict
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction import DictVectorizer


def add_feature(df):
    # Call treetagger
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')

    # Retrieve text data from dataframe
    articles = df["text"].tolist()

    # Create separate dataframe for all POS features
    pos_df = pd.DataFrame(annotate_with_pos(articles, tagger))

    # Concatenate the two dataframes
    df = pd.concat([df, pos_df], axis=1)

    return df


def annotate_with_pos(articles, tagger):
    all_pos = []

    for art in articles:
        tokenized_art = []

        # Tokenize by word
        for sent in art.split('\n'):
            tokenized_art += word_tokenize(sent)
        tg_input = "\n".join([t for t in tokenized_art])

        # Apply tagger
        tg_output = tagger.tag_text(tg_input)

        # Receive tags for each word, exclude URLs and similar
        anno = treetaggerwrapper.make_tags(tg_output, exclude_nottags=True)

        pos_dict = defaultdict(int)

        # Count the POS tag occurences
        # NOTE: Saving the list of tags caused memory errors.
        for a in anno:
            pos_dict[a[1]] += 1

        all_pos.append(pos_dict)

    vec = DictVectorizer()
    pos_vectorized = vec.fit_transform(all_pos)

    # Convert the dictionary to feature matrix
    return pos_vectorized.toarray()
