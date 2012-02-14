#!/usr/bin/env python

import MySQLdb
from MySQLdb import *

conn = MySQLdb.connect(host='localhost', user='fntennis', passwd='k2baby')

curs = conn.cursor()

curs.execute('use friday_tennis')

ret = curs.execute('select * from couples')

print "Number of rows %d\n" % curs.rowcount

colnames = [desc[0] for desc in curs.description]
couples = [dict(zip(colnames,row)) for row in curs.fetchall()]

for couple in couples:
    paID = couple['pa_id']
    pbID = couple['pb_id']
    
    ret = curs.execute("select * from players where PID in (%ld,%ld)" % (paID,pbID))
    
        
    if curs.rowcount > 0:
        colnames = [desc[0] for desc in curs.description]
        coupledata = [dict(zip(colnames,row)) for row in curs.fetchall()]
        
        couple['data'] = coupledata
    
    
    
    
    
    

