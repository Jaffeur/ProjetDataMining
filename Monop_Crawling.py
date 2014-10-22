# -*- coding: utf-8 -*-


import requests
import re
from bs4 import BeautifulSoup


def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def get_monop_rayons_1():
    R = getSoupFromUrl('http://courses.monoprix.fr/magasin-en-ligne/courses-en-ligne.html')
    R_a = R.find_all("ul", class_="SideNav")[0].find_all("a")
    R_b = [r.get('href') for r in R_a]
    rayons_1 = []
    for r in R_b:
        rayons_1.append(r.split(";")[0])
    return rayons_1

# ALIM & BOISSONS etc:
def get_monop_rayons_1_1(sous_rayon):
    R = getSoupFromUrl('http://courses.monoprix.fr/' + sous_rayon)
    R.find_all(href=re.compile("RIDB"))

######################################################################
rayons_1 = get_monop_rayons_1()

# boucle for ?? rayon[0] à rayon[4]...

# ALIM & BOISSONS -> []:
sous_rayon_alim = rayons_1[0]     # /RIDA/Alimentation-Boissons-6543255
rayons_1_1 = get_monop_rayons_1_1(sous_rayon_alim)




R.find_all(href=re.compile("RIDB"))

for sibling in R.a.next_siblings:
    print(repr(sibling))





