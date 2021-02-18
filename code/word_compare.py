# -*- coding: utf-8 -*-

# import libraries
import nltk
from itertools import chain
from nltk.corpus import wordnet
nltk.download('wordnet')

# getting root meaning of every word
wn = nltk.WordNetLemmatizer()

def checker(word1, word2):
    # print("Hello")
    # import pdb; pdb.set_trace()
    word1 = wn.lemmatize(word1.lower())
    word2 = wn.lemmatize(word2.lower())
    # generating synonym set for each word
    synonyms1 = wordnet.synsets(word1)
    syn_set1 = set(chain.from_iterable([word.lemma_names() for word in synonyms1]))
    synonyms2 = wordnet.synsets(word2)
    syn_set2 = set(chain.from_iterable([word.lemma_names() for word in synonyms2]))


    if word1 == word2:
        return word1, word2
    elif word2 in syn_set1:
        return word1, word1
    elif word1 in syn_set2:
        return word2, word2
    else:
        return "None"

if __name__ == "__main__":
    print(checker("contents","capacity"))