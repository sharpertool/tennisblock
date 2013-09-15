
import os
import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'tennisblock_dj.settings.dev'

from django.db import connection
from blockdb.models import *

class DBTeams(object):

    def __init__(self,matchid=None):

        #self.sid = self.getSeasonId()
        if matchid is not None:
            self.matchid = matchid
        else:
            self.matchid = self.getNextMatch()

    def currentSeason(self):
        seasons = Season.objects.filter(enddate__gte = datetime.date.today())
        if len(seasons) > 0:
            return seasons[0]

        return None

    def nextMeeting(self,season):
        meetings = Meetings.objects \
            .order_by('date') \
            .filter(season=season, date__gte = datetime.date.today())

        mtg = None
        if len(meetings) > 0:
            mtg = meetings[0]

        return mtg

    def getMatchid(self):
        return self.matchid

    def getPlayerID(self,name):

        f,l = name.split()
        try:
            p = Player.objects.get(first=f,last=l)

            return p

        except:
            return None

    def getNextMatch(self):

        s = self.currentSeason()
        m = self.nextMeeting(s)

        return m

    def getPlayers(self):

        m = self.getNextMatch()

        men = []
        women = []

        sched = Schedule.objects.filter(meeting=m)
        for s in sched:
            p = s.player
            if p.gender == 'F':
                women.append(p)
            elif p.gender == 'M':
                men.append(p)
            else:
                raise("No proper Geneder!")

        return men,women

    def initTeamGen(self):
        Slot.objects.filter(meeting = self.matchid).delete()
        pass

    def InsertRecords(self,seq):
        """
        Insert the sequence
        """

        self.initTeamGen()
        m = self.getNextMatch()

        # Insert the slots

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

                    slot = Slot.objects.create(
                        meeting = m,
                        set = set,
                        court = court,
                        player = pid,
                        position = position
                    )
                    slot.save()

                court = court + 1

            set = set + 1

def main():

    pass


if __name__ == '__main__':
    main()


