# -*- coding: utf-8 -*-


import requests
import re
from bs4 import BeautifulSoup


def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text, "html.parser")
    else:
        print 'Request failed', url
        return "Failed"

# rayons 1 : RIDA
url0 = 'http://courses.monoprix.fr/magasin-en-ligne/courses-en-ligne.html'
R = getSoupFromUrl(url0)
R_a = R.find_all("ul", class_="SideNav")[0].find_all("a")
R_b = [r.get('href') for r in R_a]
rayons_1 = []
for r in R_b:
    rayons_1.append(r.split(";")[0])


# rayons 2 : RIDB
url1 = 'http://courses.monoprix.fr/RIDB/Alimentation-bebe-6543256'
R = getSoupFromUrl(url1)
R_a = R.find_all(href = re.compile('RIDB'))
rayons_2 = [r.get('href').split(";")[0] for r in R_a]

# rayons 3 : RIDC
rayons_3 = []
for i in range(len(rayons_2)):
    url2 = 'http://courses.monoprix.fr/' + rayons_2[i]
    R = getSoupFromUrl(url2)
    R_a = R.find_all(href = re.compile('RIDC'))
    rayons_3.extend([r.get('href').split(";")[0] for r in R_a])

# rayons 4 : RIDC
rayons_4 = []
for i in range(len(rayons_3)):
    url3 = 'http://courses.monoprix.fr/' + rayons_3[i]
    R = getSoupFromUrl(url3)
    R_a = R.find_all(href = re.compile('RIDD'))
    rayons_4.extend([r.get('href').split(";")[0] for r in R_a])

# rayons 5 : RIDE
rayons_5 = []
for i in range(len(rayons_4)):
    url4 = 'http://courses.monoprix.fr/' + rayons_4[i]
    R = getSoupFromUrl(url4)
    R_a = R.find_all(href = re.compile('RIDE'))
    rayons_5.extend([r.get('href').split(";")[0] for r in R_a])

"***************** LISTE COMPLETE *********************"
f_w = open('Produits_Monoprix_Details','w')
url = 'http://courses.monoprix.fr'
for i in range(len(rayons_5)):
    line = rayons_5[i]
    line.rstrip()
    R = getSoupFromUrl(url + line)
    if R == "Failed":
        print "No objects, pb url..."
    else:
        R_0 = R.find("p", class_="Style02")
        if not R_0:
            f_w.write("*")
        else:
            print R_0.next_element.rstrip().encode('utf-8') + ' || '
            f_w.write(R_0.next_element.rstrip().encode('utf-8') + ' || ')

        R_1 = R.find("p", class_="Style03")
        if not R_1:
            f_w.write("*")
        else:
            f_w.write(R_1.next_element.rstrip().encode('utf-8') + ' || ')
        R_a = R.find_all("p", class_="Para04")
        for a in R_a[:len(R_a)-1]:
            if a.next_element != u' ':
                if not a:
                    f_w.write("*")
            else:
                f_w.write(a.next_element.rstrip().encode('utf-8') + ' || ' )
        f_w.write('\n')
f_w.close()


