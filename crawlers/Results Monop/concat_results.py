# -*- coding: utf-8 -*-

import pandas as pd

Produits1 = pd.read_csv("Produits_infos_1.csv", sep='|', index_col=0, encoding="utf-8")
Produits2 = pd.read_csv("Produits_infos_2.csv", sep='|', index_col=0, encoding="utf-8")
Produits3 = pd.read_csv("Produits_infos_3.csv", sep='|', index_col=0, encoding="utf-8")
Produits4 = pd.read_csv("Produits_infos_4.csv", sep='|', index_col=0, encoding="utf-8")


Produits = pd.concat([Produits1, Produits2, Produits3, Produits4], axis=0, ignore_index=True, verify_integrity=True)

Produits.apply(lambda x: x.replace(u'\n', u''))

Produits.to_csv("PRODUITS_MONOP.csv", sep='|', encoding="utf-8")


#lines = open('Produits_Monoprix_RIDE.txt', 'r').readlines()
#lines_set = set(lines)

#out  = open('Produits_Monoprix_RIDE.txt', 'w')

#for line in lines_set:
#    out.write(line)
