# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import unicodedata


def getDetails(url):

	enseigne='Simply'
	descriptif=''
	prix=''
	prix_poids=''
	origine=''
	quantite=1
	poids_volume=''
	unite=''
	poids_volume_total=''
	marque=''
	ingredients=''
	conservation=''
	valeurs_energetiques=''
	result=''
	r = requests.get(url)
	soup = BeautifulSoup(r.text,'html.parser')
	balises_div = soup.find("div", id="produit")

	if balises_div!=None:
		product_info=pd.Series(balises_div.text.split("\n"))
		
		reduced_prod_info=[]
		for k in range(product_info.shape[0]):
			if product_info[k].strip()!='':
				reduced_prod_info.append(unicodedata.normalize('NFKD', product_info[k].strip()).encode('ascii','ignore'))

		#title=re.match(r'(\D+\s)+(\d\.?\d+)?(\w+)?(.+)( - )(.+)',reduced_prod_info[0])
		reduced_prod_info[0].replace

		title=re.match(r'(.+)( - )(.+)',reduced_prod_info[0])
		if title!=None:
			nom=title.group(1)
			marque=title.group(3)
		else:
			nom=reduced_prod_info[0]

		
		title=re.match(r'(.*)\s(\d+\.?\d+?)(KG|G|ML|CL|L)',nom)
		if title!=None:
			nom=title.group(1)
			quantite=1
			poids_volume_total=title.group(2)
			unite=title.group(3)
		
		title=re.match(r'(.*)\s(\d+)(KG|G|ML|CL|L)',nom)
		if title!=None:
			nom=title.group(1)
			quantite=1
			poids_volume_total=title.group(2)
			unite=title.group(3)



		title=re.match(r'(.*)\s(\d+)X(\d+\.?\d+?)(KG|G|ML|CL|L)',nom)
		if title!=None:
			nom=title.group(1)
			quantite=title.group(2)
			poids_volume=title.group(3)
			unite=title.group(4)

		title=re.match(r'(.*)\s(\d+)X(\d+)(KG|G|ML|CL|L)',nom)
		if title!=None:
			nom=title.group(1)
			quantite=title.group(2)
			poids_volume=title.group(3)
			unite=title.group(4)

		title=re.match(r'(.*)\s(X\d+)',nom)
		if title!=None:
			nom=nom.replace(title.group(2)+' ','')
			quantite=title.group(2).replace('X','')

		title=re.match(r'(.+?)(\d+)\s(TRANCHES)(.*)',nom)
		if title!=None:
			nom=nom.replace(title.group(2)+' '+title.group(3),'')
			quantite=title.group(2)
			unite=title.group(3)

		#if title!=None:
		#	nom=title.group(1)
		#	poids_volume=title.group(2)
		#	unite=title.group(3)
		#	marque=title.group(6)
		#else:	
		#	nom=reduced_prod_info[0]

		prix_reg=re.match(r'(\d+,\d+)',reduced_prod_info[1])
		if prix_reg!=None:
			prix=prix_reg.group(1)

		prix_poids_reg=re.match(r'(\d+,\d+)',reduced_prod_info[2])
		if prix_poids_reg!=None:
			prix_poids=prix_poids_reg.group(1)

		if 'Descriptif' in reduced_prod_info:
			index_descriptif=reduced_prod_info.index('Descriptif')
			descriptif=reduced_prod_info[index_descriptif+1]

		if 'Ingredients' in reduced_prod_info:
			index_ingredients=reduced_prod_info.index('Ingredients')
			ingredients=reduced_prod_info[index_ingredients+1]
		
		if 'Conservation' in reduced_prod_info:
			index_conservation=reduced_prod_info.index('Conservation')
			conservation=reduced_prod_info[index_conservation+1]
		
		if 'Valeurs energetiques' in reduced_prod_info:
			index_energie=reduced_prod_info.index('Valeurs energetiques')
			valeurs_energetiques=reduced_prod_info[index_energie+1]

			

		result=pd.Series([enseigne, url, nom, marque, quantite, poids_volume, unite, poids_volume_total, descriptif, ingredients, conservation, valeurs_energetiques, origine, prix, prix_poids], index=['enseigne', 'url', 'nom', 'marque', 'quantite', 'poids_volume', 'unite', 'poids_volume_total', 'descriptif', 'ingredients', 'conservation', 'valeurs_energetiques', 'origine', 'prix', 'prix_poids'])

 	return result

pieces=[]
columns=['index','url']
urls=pd.read_csv('ProductLink.csv', names=columns)
liste=urls['url'].tolist()
i=1
for url in liste[5270:]:
	result=getDetails(url)
	#if type(result)!=str:
	a=pd.DataFrame(result)
	pieces.append(a.transpose())
	i=i+1
	print i 
Simply_DB = pd.concat(pieces)
Simply_DB.to_csv('Simply_DB.csv', encoding='utf-8')