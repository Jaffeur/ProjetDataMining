#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


r = requests.get("http://www.houra.fr/catalogue/?id_article=1255067")
if r.status_code == 200:
	soup = BeautifulSoup(r.text)
	balise = soup.find("div", {"id":"colorbox", "class":"", "role":"dialog"})
	print balise
	#div class="infos_produit"