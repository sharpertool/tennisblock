
import re
from DBConnection import DBConnUser

class DBTennisBlock(DBConnUser):

    def __init__(self,connection):
        super(DBTennisBlock,self).__init__(connection)

        self.season = None
        self.setTableNames()

    def setTableNames(self):

        self.tPlayers = "players"
        self.tMeetings = "blockmeetings"
        self.tCouples = "couples"
        self.tAvailability = "availability"
        self.tSchedule = "schedule"
        self.tSeasonPlayers = "season_players"
        self.tSeasons = "seasons"
        self.tSlots = "slots"

    def clearSeason(self,season):
        """
        Just delete all from the current tables.
        """

        sid = self.getSeasonId(season)

        if sid:
            curs = self.getCursor()
            curs.execute("delete from %s where sid = %d" % (self.tAvailability,sid))
            #curs.execute("alter table %s AUTO_INCREMENT=1" % self.compTable)

            curs.execute("delete from %s where sid = %d" % (self.tMeetings,sid))
            curs.execute("delete from %s where sid = %d" % (self.tMeetings,sid))
            curs.execute("delete from %s where sid = %d" % (self.tSeasonPlayers,sid))
            curs.execute("delete from %s where season = \"%s\"" % (self.tSchedule,season))
            self.conn.commit()

    def getSeasonId(self,season):
        """
        Retrieve the id for a season, if it exists.

        """

        sql = """
        select sid
        from %s
        where season = "%s"
        """ % (self.tSeasons,season)

        curs = self.getCursor()
        curs.execute(sql)
        row = curs.fetchone()
        if row:
            # This category exists..
            sid = row[0]

        else:
            sid = None

        return sid

    def addMeetings(self,season,meetings):
        """
        Add the meeting dates to the tMeetings table
        """

        sid = self.getSeasonId(season)

        if sid:
            curs = self.getCursor()

            for m in meetings:
                sql = """
                    insert into %s (
                        date, holdout, season, sid
                    ) values (
                        "%s",
                        %d,
                        "%s",
                        %d
                    )
                """ % (self.tMeetings, m['date'], int(m['holdout']), season,sid)
                curs.execute(sql)

            self.conn.commit()

    def addPlayers(self,season,players):
        """
        Add players to the season
        """

        sid = self.getSeasonId(season)

        if sid:
            curs = self.getCursor()

            for p in players:

                pid = p['PID']
                blockmember = p['blockmember']
                if pid == None:
                    pid = getPlayerId(p['First'],p['Last'])

                if pid == None:
                    pid = self.insertPlayer(p)

                if pid:
                    sql = """
                        insert into %s (
                            pid,season, blockmember, sid
                        ) values (
                            %d,
                            "%s",
                            %d,
                            %d
                        )
                    """ % (self.tSeasonPlayers, pid, season, blockmember, sid)
                    curs.execute(sql)

            self.conn.commit()

    def addCouples(self,season,couples):
        """
        Add players to the season
        """

        sid = self.getSeasonId(season)

        if sid:
            curs = self.getCursor()

            for cname in couples.keys():
                c = couples[cname]

                sql = """
                    insert into %s (
                        couplename, pa_id, pb_id, fulltime, canschedule,
                        blockcouple, season
                    ) values (
                        "%s",%d,%d,%d,%d,%d, "%s"
                    )
                """ % (self.tCouples, cname, c['pa_id'], c['pb_id'],
                        c['fulltime'], c['canschedule'], c['blockcouple'], season)
                curs.execute(sql)

            self.conn.commit()


    def insertSeason(self,season,courts,firstCourt):
        """
        Insert a new season
        """

        sql = """
            insert into %s
            (
                season,
                courts,
                firstcourt
            )

            values (
                "%s",
                %d,
                %d
            )
            """ % (self.tSeasons, season, courts, firstCourt)

        curs = self.getCursor()
        curs.execute(sql)
        sid = self.insertId()
        return sid

    def insertPlayer(self,player):
        """
        Insert a new player, with no pid.
        """

        f = player['First']
        l = player['Last']
        gen = player['Gender']
        ntrp = player['NTRP']
        untrp = player['uNTRP']

        sql = """
            insert into %s
            (
                firstname, lastname, gender, NTRP, micronNTRP
            ) values (
                "%s","%s","%s",%f, %f
            )
            """ % (self.tPlayers, f,l,gen,ntrp,untrp)

        curs = self.getCursor()
        curs.execute(sql)
        pid = self.insertId()
        return pid

    def getPlayerId(self,first,last):

        sql = """
        select pid
        from %s
        where first = "%s" and last = "%s"
        """ % (self.tPlayers,first,last)

        curs = self.getCursor()
        curs.execute(sql)
        row = curs.fetchone()
        if row:
            # This category exists..
            pid = row[0]

        else:
            pid = None

        return pid



def main():

    # Left over.. could put some test code here.
    pass


if __name__ == '__main__':
    main()
