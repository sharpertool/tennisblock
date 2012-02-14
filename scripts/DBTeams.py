

from DBManager import *
from Player import *

class DBTeams(DBConnection):

    def __init__(self,matchid=None):
        DBConnection.__init__(self,'prod')

        #self.sid = self.getSeasonId()
        if matchid is not None:
            self.matchid = matchid
        else:
            self.matchid = self.getNextMatch()

    def getMatchid(self):
        return self.matchid

    def getPlayerID(self,name):

        curs = self.getCursor()

        f,l = name.split()

        sql = 'select pid from players where firstname = "%s" and lastname = "%s"' % (f,l)

        curs.execute(sql)
        results = curs.fetchone()

        if results == None:
            return None

        return results[0]

    def getNextMatch(self):

        curs = self.getCursor()
        sql = """
            select
                min(meetid) ID
            from
                blockmeetings
            where
                date > date_sub(curdate(),interval 1 day)
                     """

        curs.execute(sql)

        results = curs.fetchone()

        if results == None:
            raise Exception("Could not determine the next match id.")

        return results[0]

    def getPlayers(self):

        curs = self.getCursor()

        sql = """

        select
            p.pid pid,
            firstname,
            lastname,
            gender,
            NTRP,
            microNTRP
        from
            players p, schedule s
        where
            matchid = %d
            and s.pid = p.pid

                     """ % (self.matchid)

        curs.execute(sql)

        players = curs.fetchallDict()

        men = []
        women = []
        for p in players:
            pObj = Player(p)
            if pObj.gender == 'm':
                men.append(pObj)
            else:
                women.append(pObj)

        return men,women

    def initTeamGen(self):

        curs = self.getCursor()
        sql = 'delete from slots where matchid = %d' % self.matchid
        curs.execute(sql)
        self.commit()

    def InsertRecords(self,seq):
        """
        Insert the sequence
        """

        self.initTeamGen()

        curs = self.getCursor()

        set = 1
        for s in seq:
            court = 1
            for m in s.matches:

                m1 = m.t1.m
                f1 = m.t1.f
                m2 = m.t2.m
                f2 = m.t2.f

                positions = {
                    'tapa'  : m1.pid,
                    'tapb'  : f1.pid,
                    'tbpa'  : m2.pid,
                    'tbpb'  : f2.pid
                }

                for position in positions.keys():
                    pid = positions[position]
                    sql = """
                        insert into slots
                            (matchid, setnum, court,pid,position,combokey)
                        values (
                            %d,
                            %d,
                            %d,
                            %d,
                            "%s",
                            ""
                        )
                            """ % (self.matchid,set,court,pid,position)

                    curs.execute(sql)
                court = court + 1

            set = set + 1

        self.commit()

def main():

    pass


if __name__ == '__main__':
    main()


