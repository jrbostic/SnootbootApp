import MySQLdb
import random

__author__ = 'jessebostic'

db = MySQLdb.connect(host = "50.62.209.116", port=3306, user="TCSS_445", passwd="L3mm31N!", db="Snootboots")

cur = db.cursor()

#cur.execute("INSERT INTO SNOOTBOOTS (Name) VALUES ('A Special Boot')")

cur.execute("SELECT * FROM SNOOTBOOTS")

for row in cur.fetchall():
    print row