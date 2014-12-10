# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import pandas as pd
import numpy
import string
import math
from textblob import TextBlob as tb
import matplotlib.pylab as plt
import os
import seaborn as sns
from stemming import Stemmer

#--------------------------------------------------------------------------------#
#                                Initialize Plot                                 #
#--------------------------------------------------------------------------------#

os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin'

plt.close("all")
dirname="results_images/"
imageformat='.png'
from matplotlib import rc
params = {'axes.labelsize': 12,
          'text.fontsize': 12,
          'legend.fontsize': 12,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True,
          'figure.figsize': (8,6),
          'text.latex.unicode' : True}
plt.rcParams.update(params)
sns.set_context("poster")
sns.set_style("white")
sns.set_palette("colorblind")
sns.set_style("ticks")

rc('font', **{'family':'serif', 'serif':['Helvetica']})
rc('text', usetex=True)

#--------------------------------------------------------------------------------#
#                                Define Functions                                #
#--------------------------------------------------------------------------------#

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

with open('stopwords_fr.txt') as f:
    Stopwords = [r.rstrip() for r in f.readlines()]

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


stemmer = Stemmer()

def DistJaccard(str1, str2):
    if str1 != '' and str2 != '':
        str1 = set(str1.split())
        str2 = set(str2.split())
        return 1.0 - float(len(str1 & str2)) / len(str1 | str2)
    else:
        return numpy.nan

#--------------------------------------------------------------------------------#
#                   Get products infos from GoldStandard                         #
#--------------------------------------------------------------------------------#

# complete Database
ProductsDB = pd.read_csv('Complete_DB.csv', encoding = 'utf8')

# Golden Standard
GoldStandard = pd.read_csv('GoldStandard.csv', sep = ';', encoding = 'utf8')
Ids = []
for i in range(GoldStandard.shape[0]):
    Ids.extend(GoldStandard.loc[i].tolist())
index_ = []
for prod_ID in Ids:
    index_.extend(ProductsDB[ProductsDB['Product-ID']== int(prod_ID)].index.tolist())
GStandard= pd.DataFrame(index = range(len(index_)), columns=ProductsDB.columns)
j = 0
for i in index_:
    GStandard.loc[j] = ProductsDB.loc[i]
    j += 1

# Products to compare:

ProdsGS_toCompare = GoldStandard['Product Simply']
Ids_tc = []
for i in range(GoldStandard.shape[0]):
    Ids_tc.append(ProdsGS_toCompare.loc[i])
index_tc = []
for prod_ID in Ids_tc:
    index_tc.extend(ProductsDB[ProductsDB['Product-ID']== int(prod_ID)].index.tolist())

Products_GS_tc = pd.DataFrame(index = range(len(index_tc)), columns=ProductsDB.columns)
j = 0
for i in index_tc:
    Products_GS_tc.loc[j] = ProductsDB.loc[i]
    j += 1

'''

#--------------------------------------------------------------------------------#
#                                  TF-IDF                                        #
#--------------------------------------------------------------------------------#

# Ingredients corpus
bloblist_ing = [tb(normalize_data(toString(ing))) for ing in (Products_GS['ingredients'].tolist() + Products_GS_tc['ingredients'].tolist())]

# Compute TfIdf for ingredients, select the 10 most important words
words_tfidf = []
for i, blob in enumerate(bloblist_ing):
    #print("Top words in document {}".format(i + 1))
    scores = {word: tfidf((word), blob, bloblist_ing) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    words = ''
    for word, score in sorted_words[:10]:
        #print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
        words += (' ' + word)
    words_tfidf.append(words)


'''

#------------------------------------------------------------------#
#                       Distance - Matrix                          #
#------------------------------------------------------------------#

## Jaccard sur les champs

ind_ = range(Products_GS_tc.shape[0])
champs = ['nom', 'ingredients', 'descriptif']
poids = [0.6, 0.2, 0.2]
#colonnes = Products_GS_tc.columns.tolist()



Result = {}
for i in ind_:
    print "\n Comparaison Produit " + str(i) + " : " + Products_GS_tc['nom'].loc[i] +"\n"
    # store the ten closest products
    Sim_Prods = pd.DataFrame(numpy.ones((10, 2)), columns=['Id', 'Distance'])
    # fill the first ten distance values
    k = 0
    for j in range(10):
        Distance = 0.0
        p = 0
        Dist = 0.0
        for champ in champs:
            Dist += DistJaccard(
                normalize_data(Products_GS_tc[champ].loc[i]) ,
                normalize_data(ProductsDB[champ].loc[j]))*poids[p]
            p += 1
        Distance = Dist
        Sim_Prods.iat[k,0] = ProductsDB['Product-ID'].loc[j]
        Sim_Prods.iat[k,1] = Distance
        k += 1

    for j in range(10, ProductsDB.shape[0]):
        if j != i:
            Distance = 0.0
            p = 0
            Dist = 0.0
            for champ in champs:
                Dist += DistJaccard(
                    normalize_data(Products_GS_tc[champ].loc[i]) ,
                    normalize_data(ProductsDB[champ].loc[j]))*poids[p]
                p += 1
            Distance = Dist
            if Distance < max(Sim_Prods['Distance']):
                print "match ! : " + ProductsDB['nom'].loc[j]
                index_max = Sim_Prods['Distance'].tolist().index(max(Sim_Prods['Distance']))
                Sim_Prods.iat[index_max,0] = ProductsDB['Product-ID'].loc[j]
                Sim_Prods.iat[index_max,1] = Distance

    Result[Products_GS_tc['Product-ID'].loc[i]] = Sim_Prods['Id'].tolist()



'''

#------------------------------------------------------------------#
#     Distance - Matrix with results of tf-idf on ingredients    #
#------------------------------------------------------------------#

## Jaccard sur la tf-idf de ingredients

ind_ = range(len(words_tfidf))

MatDist = pd.DataFrame()
MatDist = MatDist.fillna(0) # with 0s rather than NaNs
for i in ind_:
    for j in ind_:
        if i >= j:
            Dist = 0.0
            Dist += DistJaccard(
                normalize_data(words_tfidf[i]) ,
                normalize_data(words_tfidf[j]))
            MatDist.loc[i, j] = Dist

#MatDist.to_excel('TestDistance_matrix.xlsx')

Array = MatDist.as_matrix(columns=None)
Mat = numpy.matrix(Array)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_aspect('equal')
plt.title("Distance Matrix with field: TF-IDF on Ingredients",fontsize = 16)
im = plt.imshow(Mat, interpolation='nearest', cmap=plt.cm.ocean)
plt.colorbar(im, use_gridspec=True)
sns.despine()
filename="MatDist_TFIDF_Ing"
image_name=dirname+filename+imageformat
fig.savefig(image_name)

'''
