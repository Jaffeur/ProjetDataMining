# -*- coding: utf-8 -*-

## Gets list of product's url

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

url = 'http://courses.monoprix.fr'

# rayons 1 : RIDA
url0 = 'http://courses.monoprix.fr/magasin-en-ligne/courses-en-ligne.html'
R = getSoupFromUrl(url0)
R_a = R.find_all("ul", class_="SideNav")[0].find_all("a")
rayons_1 = []
for r in R_a:
    if 'RIDA' in r.get('href'):
        link = r.get('href').split(";")[0]
        rayons_1.append(link)


# rayons 2 : RIDB
with open("RIDB_Problem.txt", "a") as fw_pb:
    for i in range(len(rayons_1)):
        url1 = url + rayons_1[i]
        R = getSoupFromUrl(url1)
        if (R == "Failed") or (len(R) == 0):
                print "No objects, pb url..."
                fw_pb.write(url1)
        R_a = R.find_all(href = re.compile('RIDB'))
        rayons_2 = [r.get('href').split(";")[0] for r in R_a]
fw_pb.close()

# rayons 3 : RIDC
with open("RIDC_Problem.txt", "a") as fw_pb:
    rayons_3 = []
    for i in range(len(rayons_2)):
        url2 = 'http://courses.monoprix.fr/' + rayons_2[i]
        R = getSoupFromUrl(url2)
        if (R == "Failed") or (len(R) == 0):
            print "No objects, pb url..."
            fw_pb.write(url2)
        R_a = R.find_all(href = re.compile('RIDC'))
        rayons_3.extend([r.get('href').split(";")[0] for r in R_a])
fw_pb.close()

"""
# rayons 4 : RIDD
with open("RIDD_Problem.txt", "a") as fw_pb:
    rayons_4 = []
    for i in range(len(rayons_3)):
        url3 = 'http://courses.monoprix.fr/' + rayons_3[i]
        R = getSoupFromUrl(url3)
        if (R == "Failed") or (len(R) == 0):
            print "No objects, pb url..."
            fw_pb.write(url3)
        R_a = R.find_all(href = re.compile('RIDD'))
        rayons_4.extend([r.get('href').split(";")[0] for r in R_a])
fw_pb.close()
"""

# rayons 5 : RIDE
with open("RIDE_Problem.txt", "a") as fw_pb:
    rayons_5 = []
    for i in range(len(rayons_3)):
        url4 = 'http://courses.monoprix.fr/' + rayons_3[i]
        R = getSoupFromUrl(url4)
        if (R == "Failed") or (len(R) == 0):
            print "No objects, pb url..."
            fw_pb.write(url4)
        # test si plusieurs pages produits
        pages_pdt = R.find_all("a", attrs={"clientid":"passToAllProducts"})
        if pages_pdt:
            url_tout = 'http://courses.monoprix.fr/' + pages_pdt[0].get('href')
            R1 = getSoupFromUrl(url_tout)
            R_a = R1.find_all(href = re.compile('RIDE'))
            rayons_5.extend([r.get('href').split(";")[0] for r in R_a])
        else:
            R_a = R.find_all(href = re.compile('RIDE'))
            rayons_5.extend([r.get('href').split(";")[0] for r in R_a])
fw_pb.close()

with open("RIDE_Produits_2.txt", "a") as fw:
    for i in range(len(rayons_5)):
        fw.write(rayons_5[i] + "\n")
fw.close()
