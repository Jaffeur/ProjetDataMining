#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import mechanize
from ghost import Ghost
import requests, re, csv, sys
import pandas as pd
import numpy as np
from slugify import slugify
from selenium import webdriver
from collections import OrderedDict
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *


class Render(QWebPage):
	def __init__(self, url):
		self.app = QApplication(sys.argv)
		QWebPage.__init__(self)
		self.loadFinished.connect(self._loadFinished)
		self.mainFrame().load(QUrl(url))
		self.app.exec_()

	def _loadFinished(self, result):
		self.frame = self.mainFrame()
		self.app.quit()


################################################################
#		Classe de produit
################################################################

class Product:

	file = None

	keys = ["enseigne","url","nom_produit",
		"marque","quantite","poid_volume",
		"poid_volume_total","unite","descriptif",
		"ingredients","conservation","valeur_energetique",
		"origine","prix","prix_unitaire"
		]
	#permet de garder les cléf dans l'odre
	infos = OrderedDict.fromkeys(keys, np.nan)

	def __init__(self, enseigne, link, file):
		self.infos['enseigne'] = enseigne
		self.infos['url'] = link
		self.file = file

	def set_info(self, elem, value):
		if isinstance(value, basestring):
			value = re.sub('\n+', '\s', value.strip())
			if value == "": value = None
		self.infos[elem] = value

	def add_to_csv(self):
		sys.stdout.write('.')
		"""line = pd.Series([value for key, value in self.infos.iteritems()])
		data_frame = pd.DataFrame(line, index=self.keys).transpose()"""
		data_frame = pd.DataFrame.from_dict(self.infos, orient='index').transpose()
		data_frame.to_csv(self.file, mode='a', encoding='utf-8', header=False, sep = "|")



################################################################
#		Recherche des infos
################################################################
file_csv = "references_auchan_suite.csv"
rayon_a_list = ['bio-ecolo','hygiene-beaute','entretien', 'animaux-maison']

def record_product_infos(rayon_a, rayon_b, rayon_c, url):


	product = Product("Auchan",url, file)
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
    if rayon_a in rayon_a_list:
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
		print soup
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


def get_rayons_a(soup):
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
	data_frame.to_csv(file_csv, encoding='utf-8', sep='|', header= False)

	url = "http://www.auchandirect.fr"

	"""br = mechanize.Browser()
	br.set_handle_robots(False)   # ignore robots
	br.set_handle_refresh(False)
	response = br.open(url)
	print response.read()"""



	browser = webdriver.Firefox()
	browser.get(url+"/Accueil")
	browser.find_element_by_xpath("//*[@alt='Accéder au site']").click()
	wait = WebDriverWait(browser, 10)
	wait.until(EC.element_to_be_clickable((By.ID,'fancybox-close')))
	browser.find_element_by_id("fancybox-close").click()
	soup = BeautifulSoup(browser.execute_script("return document.documentElement.outerHTML;"))
	browser.close()

	balise_menu = soup.find("ul", {"id":"menu-principal", "class":"menu menu-horizontal"})
	list_menu = balise_menu.find_all("a", {"class":"firsta"})

	for rayon_a in list_menu:
		rayon_a_url = rayon_a.get('href')
		rayon_a_nom = rayon_a.getText()
		if len(rayon_a_url) > 3:
			get_rayons_b(rayon_a_nom.strip(), url, rayon_a_url)


if __name__ == "__main__":
	main()
