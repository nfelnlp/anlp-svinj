import nltk
import polyglot
from polyglot.text import Text
import collections as col



def extract_named_entities(entity_list, article):
    try:
        curr_entities = Text(article).entities
    except:
        #This is neccessary because polyglot has problems with some UTF-8 characters
        printable = ''.join(x for x in article if x.isprintable())
        curr_entities = Text(printable).entities

    zeroize = lambda x : (x,0)

    entity_strings = []
    for entity in curr_entities:
        entity_str = extract_chunk_string(entity,article)
        entity_strings.append(entity_str)

    
        
    zero_tuples = list(map(zeroize, entity_list))
    entity_dict = col.OrderedDict(zero_tuples)

    for entity in entity_strings:
        if entity in entity_list:
            entity_dict[entity] += 1

    snd = lambda x : x[1]

    occurence_list = list(map(snd, entity_dict.items()))
    
    return occurence_list

def extract_chunk_string(entity, article):
    start = entity.start
    end = entity.end + 1
    return article[start:end]


def add_entities(entity_dict, article):
    try:
        curr_entities = Text(article).entities
    except:
        #This is neccessary because polyglot has problems with some UTF-8 characters
        printable = ''.join([x for x in article if x.isprintable()])
        curr_entities = Text(printable).entities

    
    for entity in curr_entities:
        entity_str = extract_chunk_string(entity,article)
        if entity_str in entity_dict.keys():
            entity_dict[entity_str] += 1
        else:
            entity_dict[entity_str] = 1

    return entity_dict

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
