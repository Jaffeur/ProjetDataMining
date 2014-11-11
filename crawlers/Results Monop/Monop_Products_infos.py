# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import pandas as pd


def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text, "html.parser")
    else:
        print 'Request failed', url
        return "Failed"


url = 'http://courses.monoprix.fr'
result = pd.DataFrame(columns=["Nom", "Format", "Description", "Prix/QTE", "Prix"])
result = result.fillna(0)
row = 0
# file to write url that did'nt work properly
with open("FINAL_Produits_Problem_4.txt", "a") as f_w_pb:
    # file with urls to scrap
    for line in open('FINAL_Produits_Problem_3.txt'):
        res = []
        R = getSoupFromUrl(url + line.strip().encode('utf-8'))
        if (R == "Failed") or (len(R) == 0):
            print "No objects, pb url..."
            f_w_pb.write(line)
        else:
            # Nom
            R_0 = R.find("p", class_="Style02")
            if not R_0:
                res.append("##")
                f_w_pb.write(line)
            else:
                #print R_0.next_element.rstrip().encode('utf-8') + ' || '
                res.append(R_0.next_element.rstrip().encode('utf-8'))

            # Format
            R_1 = R.find("p", class_="Style03")
            if not R_1:
                res.append("##")
                f_w_pb.write(line)
            else:
                res.append(R_1.next_element.rstrip().encode('utf-8'))

            # Description (liste)
            R_a = R.find_all("p", class_="Para04")
            res0 = []
            for a in R_a[:len(R_a)-1]:
                if a.next_element != u' ':
                    if not a:
                        res0.append("##")
                        f_w_pb.write(line)
                    else:
                        #print a.next_element.rstrip().encode('utf-8')
                        res0.append(a.next_element.rstrip().encode('utf-8'))
            res.append(res0)

            # Prix/QTE
            R_p = R.find("p", class_="Style06")
            if not R_p:
                res.append("##")
                f_w_pb.write(line)
            else:
                res.append(R_p.next_element.rstrip().encode('utf-8'))

            # Prix
            Prix = R.find("p", class_="priceBox")
            if not Prix:
                res.append("##")
                f_w_pb.write(line)
            else:
                res.append(Prix.next_element.next_element.rstrip().encode('utf-8'))

            # add elements to dataframe
            result.loc[row] = res
        row += 1
f_w_pb.close()

result.to_csv("FINAL_PRODUITS_MONOP_4.csv", sep='|', encoding="utf-8")
