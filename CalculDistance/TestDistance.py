# -*- coding: utf-8 -*-

import distance as d
import pandas as pd
import numpy as np
import string
from slugify import slugify, Slugify
import math



ProductsDB = pd.read_csv('../Complete_DB.csv')

with open('stopwords_fr.txt') as f:
    Stopwords = [r.rstrip() for r in f.readlines()]

ProductsTest = ProductsDB.loc[385:387]

exclude = set(string.punctuation)
def remove_ponctuation(s):
    return ''.join(ch for ch in s if ch not in exclude)

def remove_stopwords(s):
    return ' '.join(word for word in s.split() if word not in set(Stopwords))


def DistJaccard(str1, str2):
    str1 = set(str1.split())
    str2 = set(str2.split())
    return 1.0 - float(len(str1 & str2)) / len(str1 | str2)

index_ = ProductsTest.index.tolist()

for i in index_:
    for j in index_:
        print remove_stopwords(remove_ponctuation(ProductsDB[['nom', 'ingredients']].loc[i]))
        #print remove_stopwords(ProductsDB['ingredients'].loc[i])
        print remove_stopwords(remove_ponctuation(ProductsDB[['nom', 'ingredients']].loc[j]))
        #print remove_stopwords(ProductsDB['ingredients'].loc[j])
        print DistJaccard(
            remove_ponctuation(ProductsDB[['nom', 'ingredients']].loc[i]) ,
            remove_ponctuation(ProductsDB[['nom', 'ingredients']].loc[j]))
