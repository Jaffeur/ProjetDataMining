#-*- coding: utf-8 -*-

# http://zetcode.com/db/postgresqlpythontutorial/
# $ sudo ln -s /Library/PostgreSQL/9.3/lib/libssl.1.0.0.dylib /usr/lib
# $ sudo ln -s /Library/PostgreSQL/9.3/lib/libcrypto.1.0.0.dylib /usr/lib


import psycopg2
import sys


con = None


#con = psycopg2.connect(database='testdb', user='postgres')
con = psycopg2.connect(user='postgres', host='localhost', password='Ge2mcaPostgres')
dbname = "testdb"

#con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()
cur.execute('CREATE DATABASE ' + dbname)
ver = cur.fetchone()
print ver
cur.close()
con.close()
