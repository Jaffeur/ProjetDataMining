# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json
import html5lib

def getRayonA(url):
	rayonA=[]
	r = requests.get(url)
	if r.status_code == 200:
		soup = BeautifulSoup(r.text)
		balises_td1=soup.find_all("td",valign="bottom")
		balises_td2=soup.find_all("td",valign="top")
		balises_td=balises_td1+balises_td2
		
		for balise_td in balises_td:
			balises_a=balise_td.find_all("a")
			for balise_a in balises_a:
				rayonA.append(balise_a.get('href'));
	else : 
		print "Connection error"
	return rayonA

def getRayonB(url):
	rayonB=[]
	r = requests.get(url)
	if r.status_code == 200:
		soup = BeautifulSoup(r.text,'html.parser')
		balises_div = soup.find_all("div",id="nav")
		for balise_div in balises_div:
			balises_a=balise_div.find_all("a")
			for balise_a in balises_a:
				rayonB.append(balise_a.get('href'))

	else : 
		print "Connection error"
	return rayonB

def getProductLink(url):
	productLink=[]
	r = requests.get(url)
	if r.status_code == 200:
		soup = BeautifulSoup(r.text,'html.parser')
		balises_div=soup.find_all("div",class_="bloc_article_float")
		for balise_div in balises_div:
			balises_a=balise_div.find_all("a",class_="LayerFA")
			for balise_a in balises_a:
				productLink.append(balise_a.get("href"))
	else : 
		print "Connection error"

	return productLink

def getInfo(productLink):
	r = requests.get(productLink)
	if r.status_code == 200:
		soup = BeautifulSoup(r.text,'html.parser')
		balises_div=soup.find_all("div",class_="infos_produit")
		print balises_div
		#marque=soup.find("span",class_="art_marque")
		#print marque
	return


#url="http://www.houra.fr/"
#a=getRayonA(url)
#b=getRayonB(str(a[0]))
#c=getProductLink(str(b[0]))
#print c[0]
url='http://www.houra.fr/btk/layer_article.php?id_article=1127494&id_origine=1446360&origine=TO_NOEUD'
r=requests.get(url)
soup=BeautifulSoup(r.text,"html5lib")
#print soup.prettify()
sleep 
print soup.find("span",{"class":"art_marque"})



