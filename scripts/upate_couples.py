#!/usr/bin/env python

import MySQLdb
from MySQLdb import *
import os

conn = MySQLdb.connect(host='localhost', user='kutenai', passwd='doulos56')

curs = conn.cursor()

curs.execute('use friday_tennis')

fp = open("couple_data.csv","r")

players = []

curs.execute('delete from couples where season = "2009 Fall";')

fields = ['cid','pa','pb','cname','fulltime','canschedule','blockcouple','season','seasonid']
sqlfields = ['cname','pa','pb','fulltime','canschedule','blockcouple','season']
lineno = 0
for line in fp:
    lineno = lineno+1
    if lineno == 1:
        continue
    lineList = line.split(',')
    
    player = dict(zip(fields,lineList))
    players.append(player)
    
for p in players:
    
    
    sql = '''\
insert
    into couples
    (couplename,pa_id,pb_id,fulltime,canschedule,blockcouple,season)
    values (
    '''
    
    vals = ",".join([p[f] for f in sqlfields])
    
    sql = sql + vals + ");"

    print sql
    curs.execute(sql)
    
conn.commit()
    

    
    
    
    
