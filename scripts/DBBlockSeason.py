#!/usr/bin/env python

import sys

import time
from DBConnection import DBConnUser

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

class DBBlockSeason(DBConnUser):

    def __init__(self,connection):
        super(DBBlockSeason,self).__init__(connection)

    def UpdateBlockMeetings(self,ws):
        r = 2
        d = ws.Cells(r,2).Value

        curs = self.getCursor()

        while d:
            ho = ws.Cells(r,3).Value
            season = ws.Cells(4,4).Value
            sid = ws.Cells(4,5).Value

            dval = time.strftime("%Y-%m-%d",time.localtime(int(d)))

            sql = """insert into blockmeetings
            (date,holdout,season,sid,comments)
            values ('{0}',{1},'{2}',{3},'');
            """.format(dval,int(ho),season,int(sid))

            curs.execute(sql)

            r = r + 1
            d = ws.Cells(r,2).Value

        curs.commit()

    def UpdateCouples(self,ws):

        curs = self.getCursor()

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
                    curs.execute(sql)

            r = r + 1
            first_her = ws.Cells(r,3).Value


    def ReadPlayers(self,ws):

        curs = self.getCursor()

        sql = "select * from `players`"

        curr.execute(sql)
        row = curr.fetchoneDict()
        rowidx = 2
        while row:
            for (field,col) in PlayerFieldColumns.items():
                ws.Cells(rowidx,col).Value = row[field]
            rowidx = rowidx + 1
            row = curr.fetchoneDict()

    def FindPlayer(self,first,last):

        sql = """
        select * from `players`
        where `firstname` = '{0}' and `lastname` = '{1}'
        """.format(first,last)

        curr = self.getCursor()
        curr.execute(sql)
        row = curr.fetchoneDict()
        if row:
            return row
        return None

    def GetPlayerData(self,ws,r):

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

    def InsertPlayer(self,wsdata):

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
        curs = self.getCursor()
        curs.execute(sql)

    def InsertSeasonPlayer(self,player,wsdata):

        sql = """
        select * from season_players
        where `pid` = {0} and `season` = '{1}'
        """.format(player['PID'],wsdata['season'])

        curr = self.getCursor()

        curr.execute(sql)
        row = curr.fetchoneDict()
        if row:
            return # It's good, we are done

        sql = """
        insert into season_players
        (pid,season,blockmember,sid)
        values ({0},'{1}',{2},{3})
        """.format(player['PID'],wsdata['season'],wsdata['blockmember'],wsdata['sid'])
        print("SQL:{0}".format(sql))

        curr.execute(sql)

    def UpdatePlayer(self,player,wsdata):
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
            self.getCursor().execute(sql)

    def UpdatePlayers(self,ws):
        rowidx = 2

        wsdata = self.GetPlayerData(ws,rowidx)
        while wsdata: # Break when firstname is None
            if not wsdata['firstname'] == 'Nobody':
                player = self.FindPlayer(wsdata['firstname'],wsdata['lastname'])
                if player:
                    self.UpdatePlayer(player,wsdata)
                else:
                    self.InsertPlayer(wsdata)
                    player = FindPlayer(wsdata['firstname'],wsdata['lastname'])

                if player and wsdata['season']:
                    self.InsertSeasonPlayer(player,wsdata)

            rowidx = rowidx + 1
            wsdata = self.GetPlayerData(ws,rowidx)

def main():
    pass
    
if __name__ == '__main__':
    main()

