import numpy as np
import nltk
from itertools import chain
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from Levenshtein import ratio
from operator import itemgetter
nltk.download('wordnet')
nltk.download('stopwords')

def neatstr(string, space=''):
    return string.replace(' ', space).strip().lower()

def maincol(classname, cols):
    cols = map(neatstr, cols)
    for idx, col in enumerate(cols):
        score = ratio(classname, col)
        if (score > 0.3) and (('name' in col) or ('title' in col)):
            return idx


def common_syns(word1, word2):
    wn = nltk.WordNetLemmatizer()
    word1 = wn.lemmatize(word1.lower())
    word2 = wn.lemmatize(word2.lower())
    
    synonyms1 = wordnet.synsets(word1)
    syn_set1 = set(chain.from_iterable([word.lemma_names() for word in synonyms1]))
    synonyms2 = wordnet.synsets(word2)
    syn_set2 = set(chain.from_iterable([word.lemma_names() for word in synonyms2]))
    if syn_set1 & syn_set2:
        return True
    else:
        return False


def closest(candidate, types):
    candidate = neatstr(candidate, space='_')
    type_list = types if type(types) == list else [types]
    closest_types = []

    type_list = list(map(neatstr, type_list))
    for tp in type_list:
        cand_in_tp = candidate in tp
        subtypes = tp.split('_')
        tp_in_cand = sum(st in candidate for st in subtypes) / len(subtypes)
        if cand_in_tp or tp_in_cand > 0:
            closest_types.append((tp, tp_in_cand))

    if closest_types:
        closest_type = closest_types[np.transpose(closest_types)[1].argmax()][0]
        # print(closest_type)
        return type_list[type_list.index(closest_type)].title()

    # for tp in type_list:
    #     closest_types.append((tp, ratio(tp, candidate)))
    # print(closest_types)
    # if max(closest_types, key=itemgetter(1))[1] > 0.5:
    #     closest_type = closest_types[np.transpose(closest_types)[1].argmax()][0]
    #     print(closest_type)
    #     return type_list[type_list.index(closest_type)]
    else:
        stop_words = set(stopwords.words('english'))
        for tp in type_list:
            subtypes = set(tp.split('_')).difference(stop_words)
            cand = set(candidate.split('_')).difference(stop_words)
            if not subtypes:
                continue

            syns = 0
            for c in cand:
                syns += sum(common_syns(c, st) for st in subtypes)

            if syns >= len(subtypes) or syns >= len(cand):
                return types[type_list.index(tp)].title()
            
        return None


# wn = nltk.WordNetLemmatizer()
# word1 = wn.lemmatize('located')

# synonyms1 = wordnet.synsets(word1)
# syn_set1 = set(chain.from_iterable([word.lemma_names() for word in synonyms1]))
# print(syn_set1)
