# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import pandas as pd
import string
import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

ProductsDB = pd.read_csv('../../GS_Pierre.csv', sep = ';', encoding = 'utf8')


with open('stopwords_fr.txt') as f:
    Stopwords = [r.rstrip() for r in f.readlines()]

ProductsTest = ProductsDB.loc[1:28]

exclude = set(string.punctuation)
def remove_ponctuation(s):
    return ''.join(ch for ch in s if ch not in exclude)

def remove_stopwords(s):
    return ' '.join(word for word in s.split() if word not in set(Stopwords))

def normalize_data(s):
    return remove_stopwords(remove_ponctuation(str(s))).upper()

def toString(sentence):
    out = ''
    if str(sentence) != 'nan':
        for word in sentence.split():
            if isinstance(word, basestring):
                out += (" " + word)
#            else:
#                out += (" " + str(word))
    return out

def DistJaccard(str1, str2):
    str1 = set(str1.split())
    str2 = set(str2.split())
    return 1.0 - float(len(str1 & str2)) / len(str1 | str2)

# Find index of element of ID = X
#index_ = ProductsDB[ProductsDB['Product-ID']==105794].index.tolist()

bloblist_nom = [tb(normalize_data(toString(nom))) for nom in (ProductsDB['nom']).tolist()]
bloblist_ing = [tb(normalize_data(toString(ing))) for ing in ProductsDB['ingredients'].tolist()]

#print tfidf('FROMAGES', tb(normalize_data(ProductsDB['ingredients'].loc[19])), normalize_data(bloblist))

for i, blob in enumerate(bloblist_nom):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(toString(word), blob, bloblist_nom) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

for i, blob in enumerate(bloblist_ing):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(toString(word), blob, bloblist_ing) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
