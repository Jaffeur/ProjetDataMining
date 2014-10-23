#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests

def get_rayons_a(url):
	r = requests.get(url)
	if r.status_code == 200:
		soup = BeautifulSoup(r.text, "html.parser")
		balise_menu = soup.find("ul", {"id":"menu-principal", "class":"menu menu-horizontal"})
		return balise_menu.find_all("a", {"class":"firsta"})
	else:
		print "Pas d'accès à l'url d'auchan"

def get_rayons_b(nom, url):
	r = requests.get(url)
	print url
	if r.status_code == 200:
		soup = BeautifulSoup(r.text, "html.parser")
		balise_top_content = soup.find("div", {"class":"top-content float-container"})
		balise_menu_listes = balise_top_content.find("div", {"class":"menu-listes"})
		balise_rayons_b = balise_menu_listes.find_all("li")
		for li in balise_rayons_b:
			print li.find("h2")
	else:
		print "Pas d'accès à l'url du rayon " , nom

def main():
	url = "http://www.auchandirect.fr"
	for rayon_a in get_rayons_a(url):
		rayon_a_url = rayon_a.get('href')
		rayon_a_nom = rayon_a.getText()
		if len(rayon_a_url) > 3:
			get_rayons_b(rayon_a_nom, url + rayon_a_url)


if __name__ == "__main__":
	main()
