#!/usr/bin/env python

import sys

import os
import sys
import re
import time

from types import *

import argparse

db_host = "bondinorth.deepbondi.net"
db_user = "fnt_user"
db_pass = "P5HJTdHt5dR2t9Q2"
db_name = "friday_tennis"

PlayerFieldColumns = {
    "PID"       :   1,
    "firstname" :   2,
    "lastname"  :   3,
    "gender"    :   4,
    "NTRP"      :   5,
    "microNTRP" :   6,
    "email"     :   7,
    "home"      :   8,
    "cell"      :   9,
    "work"      :   10
}

def sqlExec(sql,conn=None):
    myConn = False
    if not conn:
        conn = dbConn()
        myConn = True

    cursor = conn.cursor()
    cursor.execute (sql)
    cursor.close()
    if myConn:
        conn.commit()
    
def wsBlank(ws):
    url = ws.Cells(1,1).Value
    if url == None:
        return True
    return False

def FetchOneAssoc(cursor) :
    data = cursor.fetchone()
    if data == None :
        return None
    desc = cursor.description

    dict = {}

    for (name, value) in zip(desc, data) :
        dict[name[0]] = value

    return dict
        
def UpdateBlockMeetings(ws,conn=None):
    r = 2
    if not conn:
        conn = dbConn()
    d = ws.Cells(r,2).Value
    while d:
        ho = ws.Cells(r,3).Value
        season = ws.Cells(4,4).Value
        sid = ws.Cells(4,5).Value
        
        dval = time.strftime("%Y-%m-%d",time.localtime(int(d)))

        sql = """insert into blockmeetings
        (date,holdout,season,sid,comments)
        values ('{0}',{1},'{2}',{3},'');
        """.format(dval,int(ho),season,int(sid))
        
        print ("SQL:{0}".format(sql))
        sqlExec(sql,conn)
        
        r = r + 1
        d = ws.Cells(r,2).Value
        
    conn.commit()

def UpdateCouples(ws,conn=None):
    if not conn:
        conn = dbConn()

    r = 3 # Start row
    first_her = ws.Cells(r,3).Value
    while first_her:
        couplename = ws.Cells(r,2).Value
        last_her = ws.Cells(r,4).Value
        first_him= ws.Cells(4,5).Value
        last_him = ws.Cells(4,6).Value
        season = ws.Cells(4,7).Value
        blockcouple = ws.Cells(4,8).Value
        canschedule = ws.Cells(4,9).Value
        fulltime= ws.Cells(4,10).Value
        
        her = FindPlayer(first_her, last_her)
        him = FindPlayer(first_him, last_him)
        
        if her and him:

            sql = """
            select * from `couples`
            where pa_id = {0} and pb_id = {1} and season = '{2}'
            """.format(int(him['PID']),int(her['PID']),season)
            
            curr = conn.cursor()
            curr.execute(sql)
            row = FetchOneAssoc(curr)
            if not row:
                # Insert the couple
                sql = """
                insert into couples
                (couplename,pa_id,pb_id,fulltime,canschedule,blockcouple,season)
                values ('{0}',{1},{2},{3},{4},{5},'{6}')
                """.format(couplename,int(him['PID']),int(her['PID']),int(fulltime),int(canschedule),int(blockcouple),season)
                
                print("SQL:{0}".format(sql))
                sqlExec(sql)
            
        r = r + 1
        first_her = ws.Cells(r,3).Value
    
    
def ReadPlayers(ws,conn=None):
    if not conn:
        conn = dbConn()

    sql = "select * from `players`"
    
    curr = conn.cursor()
    curr.execute(sql)
    row = FetchOneAssoc(curr)
    rowidx = 2
    while row:
        for (field,col) in PlayerFieldColumns.items():
            ws.Cells(rowidx,col).Value = row[field]
        rowidx = rowidx + 1
        row = FetchOneAssoc(curr)

def FindPlayer(first,last,conn= None):
    if not conn:
        conn = dbConn()

    sql = """
    select * from `players`
    where `firstname` = '{0}' and `lastname` = '{1}'
    """.format(first,last)
    
    curr = conn.cursor()
    curr.execute(sql)
    row = FetchOneAssoc(curr)
    if row:
        return row
    return None

def GetPlayerData(ws,r):
    
    # Don't return blank data.
    tval = ws.Cells(r,2).Value
    if tval == None:
        return None
    
    data = {}
    data['PID']         = ws.Cells(r,1).Value
    data['firstname']   = ws.Cells(r,2).Value
    data['lastname']    = ws.Cells(r,3).Value
    data['gender']      = ws.Cells(r,4).Value
    data['NTRP']        = ws.Cells(r,5).Value
    data['microNTRP']   = ws.Cells(r,6).Value
    data['email']       = ws.Cells(r,7).Value
    data['home']        = ws.Cells(r,8).Value
    data['cell']        = ws.Cells(r,9).Value
    data['work']        = ws.Cells(r,10).Value
    data['season']      = ws.Cells(r,11).Value
    data['sid']         = ws.Cells(r,12).Value
    data['blockmember'] = ws.Cells(r,13).Value
    
    for fld in data.keys():
        if data[fld] == None:
            data[fld] = ''
    
    return data

def InsertPlayer(wsdata):
    
    flds = ['firstname','lastname','gender','NTRP','microNTRP','email','home','cell','work']
    sql = """insert into players
    ({0})
    """.format(",".join(flds))

    vals = []
    vals.append("'" + wsdata['firstname'] + "'")
    vals.append("'" + wsdata['lastname'] + "'")
    vals.append("'" + wsdata['gender'] + "'")
    vals.append(str(wsdata['NTRP']))
    vals.append(str(wsdata['microNTRP']))
    vals.append("'" + wsdata['email'] + "'")
    vals.append("'" + wsdata['home'] + "'")
    vals.append("'" + wsdata['cell'] + "'")
    vals.append("'" + wsdata['work'] + "'")
    
    sql = sql + """values ({0})
    """.format(",".join(vals))
        
    print("SQL:{0}".format(sql))
    sqlExec(sql)
    
def InsertSeasonPlayer(player,wsdata):
    conn = dbConn()
    sql = """
    select * from season_players
    where `pid` = {0} and `season` = '{1}'
    """.format(player['PID'],wsdata['season'])
    
    curr = conn.cursor()
    curr.execute(sql)
    row = FetchOneAssoc(curr)
    if row:
        return # It's good, we are done
    
    sql = """
    insert into season_players
    (pid,season,blockmember,sid)
    values ({0},'{1}',{2},{3})
    """.format(player['PID'],wsdata['season'],wsdata['blockmember'],wsdata['sid'])
    print("SQL:{0}".format(sql))
    sqlExec(sql,conn)
    conn.commit()
    
def UpdatePlayer(player,wsdata):
    # Check all values.. update those that do not match
    sql = """update players set 
    """
    
    bNeedsUpdate = False
    for fld in ['NTRP','microNTRP','email','home','cell','work','gender']:
        if player[fld] != wsdata[fld]:
            sql = sql + """
                `{0}` = {1}
                """.format(fld,wsdata[fld])
            bNeedsUpdate = True
                
    sql = sql + """where `first` = {0} and `last` = {1}
        """.format(wsdata['firstname'],wsdata['lastname'])
        
    if bNeedsUpdate:
        print("SQL:{0}".format(sql))
        sqlExec(sql)

def UpdatePlayers(ws):
    rowidx = 2
    
    wsdata = GetPlayerData(ws,rowidx)
    while wsdata: # Break when firstname is None
        if not wsdata['firstname'] == 'Nobody':
            player = FindPlayer(wsdata['firstname'],wsdata['lastname'])
            if player:
                UpdatePlayer(player,wsdata)
            else:
                InsertPlayer(wsdata)
                player = FindPlayer(wsdata['firstname'],wsdata['lastname'])

            if player and wsdata['season']:
                InsertSeasonPlayer(player,wsdata)

        rowidx = rowidx + 1
        wsdata = GetPlayerData(ws,rowidx)

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file",
                      help="Excel File.")

    parser.add_argument("-r", "--read",
                      help="Read From Database")

    parser.add_argument("-u", "--update",
                      help="Update To Database")

    parser.add_argument('-v','--verbose',action="store_true")

    args = parser.parse_args()

    file = args.file
    if not os.path.isfile(file):
        os.error('File %s does not exist' % file)
        print "Specified file (%s) does not exist." % file
        sys.exit(2)
        
    xl = ExcelUtils()
    xl.OpenFile(file)
        
    if args.read:
        ws = xl.GetWorksheet('Players')
        if ws:
            ReadPlayers(ws)
            
    if args.update:
        ws = xl.GetWorksheet('Block Meetings')
        if ws:
            #UpdateBlockMeetings(ws)
            pass

        ws = xl.GetWorksheet('Players')
        if ws:
            #UpdatePlayers(ws)
            pass

        ws = xl.GetWorksheet('Couples')
        if ws:
            UpdateCouples(ws)
            pass
    

if __name__ == '__main__':
    main()

