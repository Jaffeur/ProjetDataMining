#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from ghost import Ghost
import requests, re, csv, sys
import pandas as pd
import numpy as np

def stop_words_list_builder(file_r):
    data = pd.read_csv(file_r)
    print data

def no_stop_words():
    print annexe


def main():
    stop_words_fr_file = "stopwords_fr.txt"
    stop_words_list_builder(stop_words_fr_file)

if __name__ ==² "__main__":
    main()