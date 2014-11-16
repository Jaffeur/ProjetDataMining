# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from slugify import slugify, Slugify
import re
import math

def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text, "html.parser")
    else:
        print 'Request failed', url
        return "Failed"

slugify_normalize = Slugify()
slugify_normalize.safe_chars = ',./'
def normalize(s):
    return slugify_normalize(s, separator=' ')

url = 'http://courses.monoprix.fr'
result = pd.DataFrame(columns=["enseigne", "url", "nom_produit", "marque", "quantite", "poids_volume", "poids_volume_total", "unite", "descriptif", "ingredients", "conservation","valeur_energetique", "origine", "prix", "prix_au_poids"])
result = result.fillna(0)


# file to write url that did'nt work properly
with open("FINAL_Produits_Problem_3.txt", "a") as f_w_pb:
    # file with urls to scrap
    for line in open('FINAL_Produits_Problem_2.txt', 'r'):

        res = pd.DataFrame(columns=["enseigne", "url", "nom_produit", "marque", "quantite", "poids_volume", "poids_volume_total", "unite", "descriptif", "ingredients", "conservation","valeur_energetique", "origine", "prix", "prix_au_poids"])

        res.loc[0, 'url'] = url + line.rstrip().encode('utf-8')
        res.loc[0, 'enseigne'] = 'Monoprix'

        R = getSoupFromUrl(url + line.rstrip().encode('utf-8'))
        if (R == "Failed") or (len(R) == 0):
            print "No objects, pb url..."
            f_w_pb.write(line)
        else:
            # Marque
            R_marque = R.find("p", class_="Style01")
            if not R_marque:
                res.loc[0, 'marque'] = np.nan
            else:
                res.loc[0, 'marque'] = normalize(R_marque.next_element.rstrip().encode('utf-8'))
            # Nom
            R_nom = R.find("p", class_="Style02")
            if not R_nom:
                res.loc[0, 'nom_produit'] = np.nan
            else:
                res.loc[0, 'nom_produit'] = normalize(R_nom.next_element.rstrip().encode('utf-8'))

            # quantite | unite | poids_volume | poids_volume_total
            R_valeur = R.find("p", class_="Style03")
            if not R_valeur:
                res.loc[0, 'valeur'] = np.nan
                res.loc[0, 'poids_volume'] = np.nan
                res.loc[0, 'unite'] = np.nan
            else:
                val = normalize(R_valeur.next_element.rstrip().encode('utf-8'))
                res.loc[0, 'valeur'] = val
                #qte_unite = re.findall(r'(\d+\w+)', val)
                qte_unite = re.findall(r'(\d+kg)|(\d+g)|(\d+L)|(\d+cl)|(\d+ml)|(\d+ML)|(\d+l)', val)
                if qte_unite:
                    qte_unite = list(qte_unite[0])
                    qte_unite = [x for x in qte_unite if x != u''][0]
                    qte = re.findall('\d+', qte_unite)[0]
                    res.loc[0, 'poids_volume'] = int(qte)
                    split_q_u = re.split('\d+', qte_unite)
                    res.loc[0, 'unite'] = split_q_u[1]
                else:
                    res.loc[0, 'poids_volume'] = np.nan
                    res.loc[0, 'unite'] = np.nan
                qte = re.findall(r'(\s)(\d+)(\s)', val)
                if qte:
                    qte = list(qte[0])
                    quantite = qte[1]
                    res.loc[0, 'quantite'] = int(quantite)
                else:
                    res.loc[0, 'quantite'] = np.nan
                if (not math.isnan(res.loc[0, 'poids_volume'])) and (not math.isnan(res.loc[0, 'quantite'])):
                    res.loc[0, 'poids_volume_total'] = int(res.loc[0, 'poids_volume']) * int(res.loc[0, 'quantite'])
                else:
                    res.loc[0, 'poids_volume_total'] = np.nan


            # Description, Ingredients, Valeur Nutritionnelle, Conservation
            Soup = R.find_all("h4")
            elements = [normalize(x.next_element) for x in Soup]
            if u'Description' in elements:
                Desc = Soup[elements.index('Description')].next_sibling.find_all('p', class_="Para04")
                res.loc[0, 'descriptif'] = np.nan
                if Desc[0].next_element:
                    if re.findall('Origine', Desc[0].next_element):
                        Origine = Desc[0].next_element.split(':')[1]
                        res.loc[0, 'origine'] = normalize(Origine)
                        if len(Desc) > 1:
                            res.loc[0, 'descriptif'] = normalize(Desc[1].next_element)
                    else:
                        res.loc[0, 'origine'] = np.nan
                        res.loc[0, 'descriptif'] = normalize(Desc[0].next_element)

            if u'Ingredients' in elements:
                Desc = Soup[elements.index('Ingredients')].next_sibling.find_all('p', class_="Para04")
                res.loc[0, 'ingredients'] = normalize(Desc[0].next_element)
            else:
                res.loc[0, 'ingredients'] = np.nan
                if u'Composition' in elements:
                    Desc = Soup[elements.index('Composition')].next_sibling.find_all('p', class_="Para04")
                    res.loc[0, 'ingredients'] = normalize(Desc[0].next_element)
                else:
                    res.loc[0, 'ingredients'] = np.nan

            if u'Valeur nutritionnelle' in elements:
                Desc = Soup[elements.index('Valeur nutritionnelle')].next_sibling.find_all('p', class_="Para04")
                val_nut = [normalize(x.next_element.rstrip()) for x in Desc]
                res.loc[0, 'valeur_energetique'] = val_nut
            else:
                res.loc[0, 'valeur_energetique'] = np.nan

            if u'Conservation' in elements:
                Desc = Soup[elements.index('Conservation')].next_sibling.find_all('p', class_="Para04")
                res.loc[0, 'conservation'] = normalize(Desc[0].next_element)
            else:
                res.loc[0, 'conservation'] = np.nan

            # Prix/QTE
            R_prixp = R.find("p", class_="Style06")
            if not R_prixp:
                res.loc[0, 'prix_au_poids'] = np.nan
            else:
                if not R_prixp.next_element:
                    res.loc[0, 'prix_au_poids'] = np.nan
                prixqte = normalize(R_prixp.next_element.rstrip().encode('utf-8'))
                if prixqte:
                    prix_au_poids = re.match(r'^((\d+),(\d+))', prixqte).group(1)
                    prix_au_poids = prix_au_poids.replace(',', '.')
                    res.loc[0, 'prix_au_poids'] = float(prix_au_poids)
                else:
                    res.loc[0, 'prix_au_poids'] = np.nan


            # Prix
            Prix = R.find("p", class_="priceBox")
            if not Prix:
                res.loc[0, 'prix'] = np.nan
            else:
                prix = normalize(Prix.next_element.next_element.rstrip().encode('utf-8'))
                prix = prix.replace(',','.').replace(' EUR', '')
                res.loc[0, 'prix'] = float(prix)

            # add elements to dataframe
            result = pd.concat([result, res], ignore_index=True, verify_integrity=True)
f_w_pb.close()

result.to_csv("FINAL_produits_info_3.csv", sep='|', encoding="utf-8", header=True, columns=["enseigne", "url", "nom_produit", "marque", "quantite", "poids_volume", "poids_volume_total", "unite", "descriptif", "ingredients", "conservation","valeur_energetique", "origine", "prix", "prix_au_poids"])
