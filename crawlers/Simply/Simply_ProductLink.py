# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

rayonsA=[]
rayonsB=[]
rayonsC=[]
rayonsD=[]
rayonsE=[]
productLink=[]


url='http://www.livraison.simplymarket.fr/'
r = requests.get(url)
soup = BeautifulSoup(r.text,'html.parser')
#balise_div=soup.find("div",class_='diaListing')
balises_a=soup.find_all("a",class_='linkMenu')

for balise_a in balises_a:
	rayonsA.append('http://www.livraison.simplymarket.fr/'+balise_a.get('href'))

for rayonA in rayonsA:
	r = requests.get(rayonA)
	soup = BeautifulSoup(r.text,'html.parser')
	balises_a=soup.find_all("a",class_='lienProduit')
	balises_tr=soup.find_all("tr",class_='trLibelle')

	for balise_a in balises_a:
		productLink.append('http://www.livraison.simplymarket.fr/'+balise_a.get('href'))

	if balises_a==[]:
		for balise_tr in balises_tr:
			rayonsB.append('http://www.livraison.simplymarket.fr/'+balise_tr.find("a").get('href'))


for rayonB in rayonsB:
	r = requests.get(rayonB)
	soup = BeautifulSoup(r.text,'html.parser')
	balises_a=soup.find_all("a",class_='lienProduit')
	balises_tr=soup.find_all("tr",class_='trLibelle')

	for balise_a in balises_a:
		productLink.append('http://www.livraison.simplymarket.fr/'+balise_a.get('href'))

	if balises_a==[]:
		for balise_tr in balises_tr:
			rayonsC.append('http://www.livraison.simplymarket.fr/'+balise_tr.find("a").get('href'))

for rayonC in rayonsC:
	r = requests.get(rayonC)
	soup = BeautifulSoup(r.text,'html.parser')
	balises_a=soup.find_all("a",class_='lienProduit')
	balises_tr=soup.find_all("tr",class_='trLibelle')

	for balise_a in balises_a:
		productLink.append('http://www.livraison.simplymarket.fr/'+balise_a.get('href'))

	if balises_a==[]:
		for balise_tr in balises_tr:
			rayonsD.append('http://www.livraison.simplymarket.fr/'+balise_tr.find("a").get('href'))

for rayonD in rayonsD:
	r = requests.get(rayonD)
	soup = BeautifulSoup(r.text,'html.parser')
	balises_a=soup.find_all("a",class_='lienProduit')
	balises_tr=soup.find_all("tr",class_='trLibelle')

	for balise_a in balises_a:
		productLink.append('http://www.livraison.simplymarket.fr/'+balise_a.get('href'))

	if balises_a==[]:
		for balise_tr in balises_tr:
			rayonsE.append('http://www.livraison.simplymarket.fr/'+balise_tr.find("a").get('href'))


links=pd.Series(productLink)
links.to_csv('ProductLink.csv')
