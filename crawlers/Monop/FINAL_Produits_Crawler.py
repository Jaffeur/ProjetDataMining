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


url = 'http://courses.monoprix.fr'
with open("FINAL_Produits.txt", "a") as f_w:
    for line in open('Produits_Monoprix_RIDE.txt'):
        #line.rstrip()
        print line
        R = getSoupFromUrl(url + line.strip().encode('utf-8'))
        if R == "Failed":
            print "No objects, pb url..."
        else:
            R_0 = R.find("p", class_="Style02")
            if not R_0:
                f_w.write("##")
            else:
                #print R_0.next_element.rstrip().encode('utf-8') + ' || '
                f_w.write(R_0.next_element.rstrip().encode('utf-8') + ' || ')

            R_1 = R.find("p", class_="Style03")
            if not R_1:
                f_w.write("##")
            else:
                f_w.write(R_1.next_element.rstrip().encode('utf-8') + ' || ')

            R_a = R.find_all("p", class_="Para04")
            for a in R_a[:len(R_a)-1]:
                if a.next_element != u' ':
                    if not a:
                        f_w.write("##")
                    else:
                        #print a.next_element.rstrip().encode('utf-8')
                        f_w.write(a.next_element.rstrip().encode('utf-8') + ' || ')

            R_p = R.find("p", class_="Style06")
            if not R_p:
                f_w.write("##")
            else:
                f_w.write(R_p.next_element.rstrip().encode('utf-8') + ' || ')

            Prix = R.find("p", class_="priceBox")
            if not Prix:
                f_w.write("##")
            else:
                f_w.write(Prix.next_element.next_element.rstrip().encode('utf-8') + ' || ')
            f_w.write('\n')
f_w.close()
