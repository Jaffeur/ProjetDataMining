#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from ghost import Ghost
import requests, re, csv, sys
import pandas as pd
from slugify import slugify
from selenium import webdriver
from collections import OrderedDict
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

################################################################
#		Classe de produit
################################################################

class Product:

	keys = ["enseigne","url","nom_produit",
		"marque","quantite","poid_volume",
		"poid_volume_total","unite","descriptif",
		"ingredients","conservation","valeur_energetique",
		"origine","prix","prix_unitaire"
		]
	#permet de garder les cléf dans l'odre
	infos = OrderedDict.fromkeys(keys, None)


	def __init__(self, enseigne, link):
		self.infos['enseigne'] = enseigne
		self.infos['url'] = link

	def set_info(self, elem, value):
		self.infos[elem] = value

	def add_to_csv(self):
		sys.stdout.write('.')
		line = pd.Series([value for key, value in self.infos.iteritems()])
		data_frame = pd.DataFrame(line).transpose()
		with open('references_auchan.csv', 'a') as csvfile:
			data_frame.to_csv(csvfile, encoding='utf-8', header=False)


################################################################
#		Recherche des infos
################################################################

def record_product_infos(rayon_a, rayon_b, rayon_c, url):
	product = Product("Auchan",url)
	#print url
	r = requests.get(url)
	if r.status_code ==200:
		soup = BeautifulSoup(r.text)
		titre_p =  soup.find("span", {"class":"titre-principal"})
		if titre_p != None: product.set_info('marque', titre_p.getText())
		titre_a = soup.find("span", {"class":"titre-annexe"})
		if titre_a != None: product.set_info('nom_produit', titre_a.getText())
		prix = soup.find("div", {"class":"prix-actuel"})
		if prix != None: product.set_info('prix', prix.getText())
		prix_a = soup.find("div", {"class":"prix-annexe"})
		if prix_a != None: product.set_info('prix_unitaire', prix_a.getText())
		quantite_unit = soup.find("span", {"class":"texte-info-normal"})
		if quantite_unit != None:
			quantite = re.search(r'(Composition\s:)(\s\d+)?(\s?(x|X))?(\s?\d+((\.|\,)\d+)?)(\s?\w*)?', quantite_unit.getText())
			if quantite:
				product.set_info('quantite', quantite.group(2))
				product.set_info('poid_volume', quantite.group(5))
				if quantite.group(2) != None:
					product.set_info('poid_volume_total', float(re.sub(',', '.',quantite.group(2)))*float(re.sub(',', '.',quantite.group(5))) )
				else:
					product.set_info('poid_volume_total', float(re.sub(',', '.',quantite.group(5))) )
					product.set_info('unite', quantite.group(8) )

		infos_detaillees = soup.find("div", {"id":"panel-infos-detaillees"})
		if infos_detaillees != None:
			h3s = infos_detaillees.find_all("h3")
			for h3 in h3s:
				if  re.search('ingredients', slugify(h3.getText().strip())):
					product.set_info('ingredients', h3.findNext('p').getText())
				elif re.search('donnees-nutritionnelles', slugify(h3.getText().strip())):
					product.set_info('valeur_energetique', h3.findNext('p').getText())
				elif re.search('informations-pratiques', slugify(h3.getText().strip())):
					product.set_info('descriptif', h3.findNext('p').getText())
				elif re.search('informations-de-conservation', slugify(h3.getText().strip())):
					product.set_info('conservation', h3.findNext('p').getText())

		prix = soup.find("div", {"class":"prix-actuel"})
		if prix != None:
			prix_regex = re.search(r'((\d+)\.?(\d+)?)', prix.getText())
			product.set_info('prix', float(prix_regex.group(0)))
		prix_unitaire = soup.find("div", {"class":"prix-annexe"})
		if prix_unitaire != None:
			prix_unit_regex = re.search(r'((\d+)\.?(\d+)?)', prix_unitaire.getText())
			product.set_info('prix_unitaire', float(prix_unit_regex.group(0)))

		product.add_to_csv()
	else:
		print "Pas d'accès à l'url " , url

def get_products(rayon_a, rayon_b, rayon_c, url, url_c):
	print "\n\t\t", rayon_c
	r = requests.get(url+url_c)
	if r.status_code == 200:
		soup = BeautifulSoup(r.text)
		balise_container = soup.find("div", {'id':"liste-produits-grille", 'class':"liste clear-container"})
		if balise_container != None:
			balises_prod = balise_container.find_all("div", {"class":"bloc-produit"})
			for prod in balises_prod:
				link = prod.find("a", {"title":"Voir le produit"}).get('href')
				record_product_infos(rayon_a, rayon_b, rayon_c, url+link)
	else:
		print "Pas d'accès à l'url " , url+url_c

def get_rayons_c(rayon_a, rayon_b, url, url_b):
	print "\n\t", rayon_b
	r = requests.get(url + url_b)
	if r.status_code == 200:
		soup = BeautifulSoup(r.text, "html.parser")
		balise_bloc = soup.find("div", {'class':"bloc_5_prd"})
		balises_prod = balise_bloc.find_all("div", {"class":"bloc_prd"})
		for prod in balises_prod:
			a = prod.find("h2").find("a")
			link = a.get('href')
			rayon_c = a.getText()
			get_products(rayon_a, rayon_b, rayon_c, url, link )
	else:
		print "Pas d'accès à l'url " , url+url_b

def get_rayons_b(nom, url, url_b):
	print "\n",nom
	r = requests.get(url+url_b)
	if r.status_code == 200:
		soup = BeautifulSoup(r.text, "html.parser")
		balise_top_content = soup.find("div", {"class":"top-content float-container"})
		balise_menu = balise_top_content.find("div", {"class":"menu-listes"}).find("ul", {"class":"menu menu-horizontal"})
		balises_rayons_b = balise_menu.findChildren()
		for rayon_b in balises_rayons_b:
			li = rayon_b.findChildren("h2")
			if len(li) > 0 :
				balise_a = li[0].findChildren("a")
				get_rayons_c(nom, balise_a[0].getText().strip(), url, balise_a[0].get('href'))
	else:
		print "Pas d'accès à l'url " , url


def get_rayons_a(url):

	r = requests.get(url)
	if r.status_code == 200:
		soup = BeautifulSoup(r.text, "html.parser")
		balise_menu = soup.find("ul", {"id":"menu-principal", "class":"menu menu-horizontal"})
		return balise_menu.find_all("a", {"class":"firsta"})
	else:
		print "Pas d'accès à l'url d'auchan"



def main():

	#Titre des attributs dans le
	line = pd.Series(["enseigne","url","nom_produit", "marque", "quantite",
	"poid_volume","poid_volume_total","unite","descriptif","ingredients",
	"conservation","valeur_energetique","origine","prix","prix_unitaire"])
	data_frame = pd.DataFrame(line).transpose()
	data_frame.to_csv('references_auchan.csv', encoding='utf-8', header=False)

	url = "http://www.auchandirect.fr"

	"""browser = webdriver.Firefox()
	browser.get(url)
	browser.find_element_by_xpath("//*[@alt='Accéder au site']").click()
	wait.until(EC.element_to_be_clickable((By.ID,'fancybox-close')))
	#browser.find_element_by_id("fancybox-close").click()

	browser.close()
	print url
	get_rayons_a(url)
	rayon_a = get_rayons_a(url+"/Accueil")[1]
	rayon_a_url = rayon_a.get('href')
	rayon_a_nom = rayon_a.getText()
	get_rayons_b(rayon_a_nom.strip(), url, rayon_a_url)"""

	for rayon_a in get_rayons_a(url+"/Accueil"):
		rayon_a_url = rayon_a.get('href')
		rayon_a_nom = rayon_a.getText()
		if len(rayon_a_url) > 3:
			get_rayons_b(rayon_a_nom.strip(), url, rayon_a_url)


if __name__ == "__main__":
	main()
