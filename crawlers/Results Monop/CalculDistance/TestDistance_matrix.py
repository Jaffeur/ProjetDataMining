# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import pandas as pd
import numpy
import string
import math
from textblob import TextBlob as tb
import matplotlib.pylab as plt

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

def DistJaccard(str1, str2):
    str1 = set(str1.split())
    str2 = set(str2.split())
    return 1.0 - float(len(str1 & str2)) / len(str1 | str2)


index_ = range(26)
groups = [index_[0:8], index_[9:17], index_[18:26]]
champs = ['nom', 'ingredients', 'descriptif']

colnames = []
for k in range(len(groups)):
    for i in range(9):
            colnames.append(str(k+1)+'_'+str(i+1))

MatDist = pd.DataFrame(index=colnames[0:len(colnames)-1], columns=colnames[0:len(colnames)-1])
MatDist = MatDist.fillna(0) # with 0s rather than NaNs


for i in index_:
    for j in index_:
        Dist = 0.0
        for champ in champs:
            Dist += DistJaccard(
                normalize_data(ProductsDB[champ].loc[i]) ,
                normalize_data(ProductsDB[champ].loc[j]))/3
        MatDist.loc[colnames[i], colnames[j]] = Dist

MatDist.to_excel('TestDistance_matrix.xlsx')

Array = MatDist.as_matrix(columns=None)
Mat = numpy.matrix(Array)
fig = plt.figure()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_aspect('equal')
plt.imshow(Mat, interpolation='nearest', cmap=plt.cm.ocean)
plt.colorbar()
plt.show()
