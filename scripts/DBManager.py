
import os
import json
import re
import MySQLdb
from time import time,mktime,strptime
from datetime import datetime,timedelta

class DBCursor:

    def __init__(self,conn):
        self.curs = None
        if conn:
            try:
                self.curs = conn.cursor()
                self.curs.execute('use friday_tennis')
            except MySQLdb.Error as e:
                print "Failed to get cursor. MySQLdb error: %d:%s" % (e.args[0], e.args[1])

            self.conn = conn

        if not self.curs:
            raise "Could not create a DB Cursor.."

    def __del__(self):
        pass

    def cursor(self):
        return self.curs

    def execute(self,sql):
        if self.curs:
            self.curs.execute(sql)

    def fetchone(self):
        if self.curs is None: raise "Cursor invalid"
        return self.curs.fetchone()

    def fetchoneDict(self):
        """
        Return a row from the cursor formatted as a dictionary.

        This function was taken from this site:
          http://www.halfcooked.com/mt/archives/000969.html


        Give credit, where credit due!
        """
        if self.curs is None: raise "Cursor invalid."

        row = self.curs.fetchone()
        if row is None: return None
        cols = [ d[0] for d in self.curs.description ]
        return dict(zip(cols, row))

    def fetchallDict(self):
        """
        Fetch all rows as an array of dictionaries.
        """

        rows = []
        row = self.fetchoneDict()
        while row:
            rows.append(row)
            row = self.fetchoneDict()

        return rows

    def fetchallObj(self):
        """
        Fetch all rows as an array of objects.
        """

        class DBRow:
            def __init__(self,row):
                self.row = row
            def __getattr__(self,item):
                if self.row.has_key(item):
                    return self.row[item]
                raise Exception("Item %s does not exist." % item)
            def __repr__(self):
                s = "DBRow "
                s = s + ";".join([key + ":" + str(self.row[key]) for key in self.row.keys()])
                return s

        rows = []
        row = self.fetchoneDict()
        while row:
            rows.append(DBRow(row))
            row = self.fetchoneDict()

        return rows

    def updateRow(self, table, **data):
        """
        Return a row from the cursor formatted as a dictionary.

        This function was taken from this site:
          http://www.halfcooked.com/mt/archives/000969.html


        Give credit, where credit due!
        """

        if self.curs is None: raise "Cursor invalid."

        idName = table + "_id"
        id = data[idName]
        del data[idName]
        sets = []
        for key in data.keys():
            sets.append("%s = %%s" % key)
            set = ', '.join(sets)
            qq = "UPDATE %s SET %s WHERE %s = %%s" % (table, set, idName,)
            self.curs.execute(qq, tuple(data.values()+[id]))

    def insertRow(self, table, **data):
        """
        Return a row from the cursor formatted as a dictionary.

        This function was taken from this site:
          http://www.halfcooked.com/mt/archives/000969.html


        Give credit, where credit due!
        """

        if self.curs is None: raise "Cursor invalid."

        keys = ', '.join(data.keys())
        vals = ', '.join(["%s"] * len(data.values()))
        qq = "INSERT INTO %s (%s) VALUES (%s)" % (table, keys, vals)
        self.curs.execute(qq, tuple(data.values()))
        return self.curs.lastrowid

    def insert_id(self):
        """
        Retreive the last insert Id from the connection.
        """
        return self.conn.insert_id()

class DBConnection:

    def __init__(self,dest="prod"):

        if dest == 'prod':
            self.hosts = [
                {'host':'192.168.1.150','port':3306},
            ]

            self.user = 'kutenai'
            self.pw = 'k2baby'
        else:
            raise "Invalid DB Destination"

        self.conn = None
        self.curs = None

    def __del__(self):
        if self.conn:
            MySQLdb.connection.close(self.conn)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def getConnection(self):
        """
        Return the current connect. Open one if none exists.

        Note that an SSH tunnel is required to  make this work..
        That tunnel must be setup on the local host before executing the script
        The hostname is eeweb.com, and the tunnel must forward local 3316 to
        the remote 3306

        P.S. - I changed the local forward port to 3316.
        """

        if self.conn == None:
            try:
                conn = None
                for hostval in self.hosts:
                    host = hostval['host']
                    port = hostval['port']
                    try:
                        print "Trying DB connection to %s at %d" % (host,port)
                        conn = MySQLdb.connect(host=host,
                                               port=port,
                                               user=self.user,
                                               passwd=self.pw)
                    except MySQLdb.Error as e:
                        conn = None
                        pass

                    if conn:
                        break


                if not conn:
                    raise Exception("Failed to open Database connection.","-1001")
                else:
                    self.conn = conn

            except MySQLdb.Error as e:
                print "Failed to open connection. MySQLdb error: %d:%s" % (e.args[0], e.args[1])
            except:
                return None
        return self.conn

    def getCursor(self):
        """
        Return a cursor and use the proper database.
        """

        conn = self.getConnection()

        if not conn:
            raise Exception("Could not establish Database connection.",'-1000')

        return DBCursor(conn)


class DBSeason(DBConnection):

    def __init__(self,currSeason,bStart, bEnd, bHoldouts):
        DBConnection.__init__(self,'prod')

        self.currSeason = currSeason
        self.bStart = bStart
        self.bEnd = bEnd
        self.bHoldouts = bHoldouts

        self.sid = self.getSeasonId()


    def isHoldout(self,date):

        for ho in self.bHoldouts:
            hoDate = datetime.strptime(ho,'%Y/%m/%d')
            if date == hoDate:
                return True
        return False

    def getSeasonId(self):

        curs = self.getCursor()

        sql = 'select sid from seasons where season = "%s"' % self.currSeason['name']

        curs.execute(sql)
        results = curs.fetchone()

        if not results:
            sid = self.insertSeason()
        else:
            sid = results[0]

        return sid

    def getSeasonName(self):

        return self.currSeason['name']

    def insertSeason(self):

        name = self.currSeason['name']
        courts = self.currSeason['courts']
        nCourts = len(courts)
        firstCourt = courts[0]

        sql = """
            insert into seasons
                (season,courts,firstcourt)
            values
                ("%s",%d,%d)
                """ % (name,nCourts,firstCourt)

        curs = self.getCursor()

        curs.execute(sql)
        sid = curs.insert_id()
        self.commit()
        return sid


    def getPlayerID(self,name):

        curs = self.getCursor()

        f,l = name.split()

        sql = 'select pid from players where firstname = "%s" and lastname = "%s"' % (f,l)

        curs.execute(sql)
        results = curs.fetchone()

        if results == None:
            return None

        return results[0]

    def verifyPlayers(self,couples):

        bAllGood = True
        for coupleName in couples:
            couple = couples[coupleName]
            for p in ['m','f']:
                person = couple[p]
                pid = self.getPlayerID(person)
                if pid:
                    print("Verified %s at %d" % (person,pid))
                else:
                    print("Play name %s not found" % person)
                    bAllGood = False

        return bAllGood


    def insertCouple(self,coupleName, him,her, fullTime):

        curs = self.getCursor()

        self.insertPlayer(him);
        self.insertPlayer(her);

        season = self.getSeasonName()

        sql = """
            insert into couples
                (couplename,pa_id,pb_id,fulltime,canschedule,blockcouple,season)
            values
                ("%s",%d,%d,%d,1,1,"%s")
             """ % (coupleName,him,her,fullTime,self.getSeasonName())

        curs.execute(sql)
        self.commit()


    def insertPlayer(self,pid):

        curs = self.getCursor()
        sql = """
            insert into season_players
                (pid,season,blockmember,sid)
            values
                (%d,"%s",1,%d)
                """ % (pid,self.getSeasonName(),self.sid)

        curs.execute(sql)

    def insertCouples(self,couples):

        self.deleteCouplesAndPlayers()

        for coupleName in couples:
            couple = couples[coupleName]

            him = couple['m']
            her = couple['f']
            split = couple['split']

            if split == "Full":
                fullTime = 1
            else:
                fullTime = 0

            him_pid = self.getPlayerID(him)
            her_pid = self.getPlayerID(her)

            self.insertCouple(coupleName, him_pid, her_pid, fullTime)

            print "Inserted %s" % coupleName

    def insertBlockMeetings(self):

        self.deleteMeetings()

        first = strptime(self.bStart,'%Y/%m/%d')

        last = strptime(self.bEnd,'%Y/%m/%d')

        curs = self.getCursor()
        curr = first
        weekDiff = timedelta(weeks=1)
        dtLast = datetime.fromtimestamp(mktime(last))
        dtCurr = datetime.fromtimestamp(mktime(curr))
        while (dtCurr < dtLast):
            if self.isHoldout(dtCurr):
                ho = 1
            else:
                ho = 0

            meeting = dtCurr.strftime("%Y-%m-%d")

            sql = """
            insert into blockmeetings
                (date,holdout,comments,season,sid)
            values
                ("%s",%d,"","%s",%d)
                 """ % (meeting,ho,self.getSeasonName(),self.sid)
            curs.execute(sql)
            self.commit()
            print "Inserted block meeting for %s" % meeting

            dtCurr = dtCurr+ weekDiff


    def deleteMeetings(self):

        curs = self.getCursor()
        curs.execute('delete from blockmeetings where season = "%s"' % self.getSeasonName())
        self.commit()

    def deleteCouplesAndPlayers(self):

        curs = self.getCursor()
        curs.execute('delete from season_players where sid = %d' % self.sid)
        curs.execute('delete from couples where season = "%s"' % self.getSeasonName())
        self.commit()


def main():

    pass


if __name__ == '__main__':
    main()
