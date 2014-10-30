# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup


def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text, "html.parser")
    else:
        print 'Request failed', url
        return "Failed"


url = 'HTTP://courses.monoprix.fr'
with open("FINAL_Produits_2.txt", "a") as f_w:
    for line in open('Produits_Monoprix_RIDE.txt'): # Liste d'URL de Produits
        print line
        R = getSoupFromUrl(url + line.strip().encode('utf-8'))
        if R == "Failed":
            print "No objects, pb url..."
        else:
            # get Product Name
            Marque = R.find("p", class_="Style01")
            if not Marque:
                f_w.write("##")
            else:
                #print R_0.next_element.rstrip().encode('utf-8') + ' || '
                f_w.write(Marque.next_element.rstrip().encode('utf-8') + ' || ')
            # Description
            Nom = R.find("p", class_="Style02")
            if not Nom:
                f_w.write("##")
            else:
                #print R_0.next_element.rstrip().encode('utf-8') + ' || '
                f_w.write(Nom.next_element.rstrip().encode('utf-8') + ' || ')

            # Description
            Desc1 = R.find("p", class_="Style03")
            if not Desc1:
                f_w.write("##")
            else:
                f_w.write(Desc1.next_element.rstrip().encode('utf-8') + ' || ')
            # Description || Conseil || Ingrédients || Valeur nutritionnelle || Conservation
            Desc2 = R.find_all("p", class_="Para04")
            for a in Desc2[:len(Desc2)-1]:
                if a.next_element != u' ':
                    if not a:
                        f_w.write("##")
                    else:
                        #print a.next_element.rstrip().encode('utf-8')
                        f_w.write(a.next_element.rstrip().encode('utf-8') + ' || ')

            # Prix au Kilo
            R_p = R.find("p", class_="Style06")
            if not R_p:
                f_w.write("##")
            else:
                f_w.write(R_p.next_element.rstrip().encode('utf-8') + ' || ')

            # Prix
            Prix = R.find("p", class_="priceBox")
            if not Prix:
                f_w.write("##")
            else:
                f_w.write(Prix.next_element.next_element.rstrip().encode('utf-8') + ' || ')
            f_w.write('\n')
f_w.close()
