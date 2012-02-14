#!/usr/bin/env python

import MySQLdb
from MySQLdb import *
import os

conn = MySQLdb.connect(host='localhost', user='kutenai', passwd='doulos56')

curs = conn.cursor()

curs.execute('use friday_tennis')

fp = open("playerdata.csv","r")

fields = ['pid','firstname','lastname','gender','NTRP','uNTRP','Cell','Home','Email','seasonPlayer','Couple','BCouple']
lineno = 0
for line in fp:
    lineno = lineno+1
    if lineno == 1:
        continue
    lineList = line.split(',')
    
    player = dict(zip(fields,lineList[0:10]))
    
    if player.has_key('seasonPlayer') and player['seasonPlayer'] == '1':
        
        sql = '''\
    insert
        into season_players
        (pid,season,blockmember,sid)
        values (%s,"%s",%d,%d)
        ''' % (player['pid'],"2009 Fall", 1, 3)
       
        curs.execute("select * from season_players where pid = %s" % player['pid'])
        
        if curs.rowcount == 0:
            print sql
            curs.execute(sql)
    
conn.commit()
    

    
    
    
    
