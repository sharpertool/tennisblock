#!/usr/bin/env python

import MySQLdb
from MySQLdb import *

conn = MySQLdb.connect(host='localhost', user='fntennis', passwd='k2baby')

curs = conn.cursor()

curs.execute('use friday_tennis')

ret = curs.execute('select * from players')

print "Number of rows %d\n" % curs.rowcount

colnames = [desc[0] for desc in curs.description]
players = [dict(zip(colnames,row)) for row in curs.fetchall()]

fp = open("playerdata.csv",'w')
fp.write("pid,First,Last,Gender,NTRP,uNTRP,Cell,Home,E-mail\n")
ret = curs.execute('select * from players')

for player in players:
    pdata = [player[k] for k in ['PID','firstname','lastname','gender','NTRP','microNTRP','cell','home','email']]
    s = "%ld,%s,%s,%s,%f,%f,%s,%s,%s\n" % (pdata[0],pdata[1],pdata[2],pdata[3],pdata[4],pdata[5],pdata[6],pdata[7],pdata[8])
    fp.write(s)        
    
fp.close()
    
    
    
    
    
    

