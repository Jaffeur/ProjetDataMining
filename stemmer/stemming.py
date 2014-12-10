#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  re, csv, sys
import pandas as pd
import numpy as np
from slugify import slugify
###############
from nltk.stem.snowball import FrenchStemmer

"""
""	Class that stems a french text
	How to use:
	stemmer = Stemmer() #initialize
	stemmer.stem("text") #return the stemmed text (str)
"""
class Stemmer:

	stop_words = []

	def __init__(self):
		self.stop_words = np.squeeze(pd.read_csv("stopwords_fr.txt").as_matrix())

	#Delete stop words, accents, specials characters, ponctuation
	def no_stop_words(self, text):
		if text != None:
			words = re.split("\s+|\p{Latin}+|[&\"#''\{\}`_^°]+", text.lower())
			texte_nst = ""
			for word in words:
				if word not in self.stop_words and not re.match("\d+",word):
					texte_nst += word + " "
			return slugify(texte_nst, separator=" ")
		else: return ""

	#return the lemme of a given french word
	def lemmatize(self, word):
		stemmer = FrenchStemmer()
		return stemmer.stem(word)

	#return a complete stemmed french text
	def stem(self, text):
		clean_text = self.no_stop_words(text)
		splited_text = clean_text.split()
		stemmed_text = ""
		for word in splited_text:
			if self.lemmatize(word) != None or self.lemmatize(word) != "":
				stemmed_text += self.lemmatize(word) + " "
		return stemmed_text.strip()

