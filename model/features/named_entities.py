import nltk
import polyglot
from polyglot.text import Text
import collections as col
import os
import ast
import pandas as pd
from sklearn.utils import shuffle


def add_features(df):
    
    train_df = df[df['split'] == "train"]
    test_df = df[df['split'] == "test"]
    

    train_articles = train_df["text"].tolist()
    train_paths = train_df["file"].tolist()

    entity_dict_list = []
    for art, path in zip(train_articles, train_paths):
        entities_dict = all_named_entities(art, path)
        entity_dict_list.append(entities_dict)

    most_common_ne, entities = most_common_entities(entity_dict_list, number=200)

    ne_features_train = pd.DataFrame(entities)

    train_df.reset_index(drop=True, inplace=True)
    ne_features_train.reset_index(drop=True, inplace=True)
    train_df = pd.concat([train_df, ne_features_train], axis=1)
    train_df['split'] = "train"


    test_articles = test_df["text"].tolist()
    test_paths = test_df["file"].tolist()

    entities = []
    for art, path in zip(test_articles, test_paths):
        occurences = extract_named_entities(most_common_ne, art, path)
        entities.append(occurences)

    ne_features_test = pd.DataFrame(entities)

    test_df.reset_index(drop=True, inplace=True)
    ne_features_test.reset_index(drop=True, inplace=True)
    test_df = pd.concat([test_df, ne_features_test], axis=1)
    test_df['split'] = "test"
    
    

    df = pd.concat([train_df, test_df])
    df = shuffle(df).reset_index(drop=True)

    
    return df

    



#extracts entities from article and extracts the corresponding strings
def entity_strings(article):
    try:
        curr_entities = Text(article).entities
    except:
        #This is neccessary because polyglot has problems with some UTF-8 characters
        printable = ''.join(x for x in article if x.isprintable())
        curr_entities = Text(printable).entities

    entity_strings = []
    for entity in curr_entities:
        entity_str = extract_chunk_string(entity,article)
        entity_strings.append(entity_str)

    return entity_strings

#extracts all named entities from an article
def all_named_entities(article, path=None):

    if not path:
        entities_dict = col.defaultdict(int)
        for entity in entity_strings(article):
            if entity == '':
                continue
            entities_dict[entity] += 1

        return entities_dict
    
    path_components = path.split("/")
    
    outlet = path_components[4]
    curr_name = path_components[6]

    entities_path = "../named_entities_data/" + outlet + "/" + curr_name + ".ne"
    
    try:
        with open(entities_path, "r") as entities_file:
            entities_str = entities_file.read()
            entities_dict = ast.literal_eval(entities_str)
            #entities_dict = eval(entities_str)
        return entities_dict
    except SyntaxError:
        print(entities_path)
        raise(SyntaxError)
    except FileNotFoundError:
        with open(entities_path, "w") as entities_file:
            entities_dict = col.defaultdict(int)
            for entity in entity_strings(article):
                if entity == '':
                    continue
                entities_dict[entity] += 1

            entities_file.write(str(entities_dict)[27:-1])
        return entities_dict
    

#extracts ony the entities in article that appear in entity_list
#end returns list with number of occurences for each of these
def extract_named_entities(entity_list, article, path):

    zeroize = lambda x: (x,0)
    
    zero_tuples = list(map(zeroize, entity_list))
    entity_dict = col.OrderedDict(zero_tuples)

    for entity, occurences in all_named_entities(article, path).items():
        if entity in entity_list:
            entity_dict[entity] = occurences

    snd = lambda x : x[1]

    occurence_list = list(map(snd, entity_dict.items()))
    
    return occurence_list

def extract_chunk_string(entity, article):
    start = entity.start
    end = entity.end
    tokenized = nltk.word_tokenize(article)
    chunk_string = " ".join(tokenized[start:end])
    return chunk_string



def insert_ordered(entity_list, entity_tuple):
    entity, occurences = entity_tuple
    greater = []
    lesser = []

    for (ent, occ) in entity_list:
        if occ > occurences:
            greater.append((ent,occ))
        else:
            lesser.append((ent,occ))

    entity_list = greater + [(entity,occurences)] + lesser

    return entity_list


def dict_add(dict1, dict2):
    for (key, value) in dict2.items():
        if key in dict1.keys():
            dict1[key] += value
        else:
            dict1[key] = value

    return dict1


#def most_common_entities(entities_left, entities_right, number=200):
def most_common_entities(entity_dict_list, number=200):
    combined_dict = col.defaultdict(int)

    for entity_dict in entity_dict_list:#entities_left + entities_right:
        combined_dict = dict_add(combined_dict, entity_dict)
    
    most_common_ne = get_most_common(combined_dict, number)


    
    #keep only most common occurences of entities from articles
    entity_vecs = []
    for entity_dict in entity_dict_list:
        entities_vec = []
        for entity in most_common_ne:
            if entity in entity_dict.keys():
                entities_vec.append(entity_dict[entity])
            else:
                entities_vec.append(0)
        entity_vecs.append(entities_vec)

    #entity_vecs_right = []
    #for entity_dict in entities_right:
    #    entities_vec = []
    #    for entity in most_common_ne:
    #        if entity in entity_dict.keys():
    #            entities_vec.append(entity_dict[entity])
    #        else:
    #            entities_vec.append(0)
    #    entity_vecs_right.append(entities_vec)

    return most_common_ne, entity_vecs
                

def get_most_common(entity_dict, number=200):
    entity_list = []
    for entity, occurences in entity_dict.items():
        if len(entity_list) <= number:
            entity_list = insert_ordered(entity_list, (entity, occurences))
        else:
            _, least_occ = entity_list[number - 1]
            if occurences > least_occ:
                entity_list = entity_list[:(number -1)]
                entity_list = insert_ordered(entity_list, (entity, occurences))

    strip_numbers = lambda ent_tuple : ent_tuple[0]
    entities_without_numbers = list(map(strip_numbers, entity_list))

    return entities_without_numbers
