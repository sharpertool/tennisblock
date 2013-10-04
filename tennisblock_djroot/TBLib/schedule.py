import os
import datetime
os.environ['PYTHONPATH'] = '../../gbrest'
os.environ['DJANGO_SETTINGS_MODULE'] = 'tennisblock_dj.settings.dev'
import random

from django.db import connection
from blockdb.models import *

import tennisblock_dj.settings.dev

class Scheduler(object):

    def __init__(self):
        pass


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

    def getFulltimeCouples(self, mtg):

        ftavailable = []
        ftcouples = Couple.objects.filter(fulltime = True,blockcouple=True)
        for c in ftcouples:
            male_av = Availability.objects.get(meeting = mtg,player = c.male)
            female_av = Availability.objects.get(meeting = mtg,player = c.female)
            if male_av.available and female_av.available:
                ftavailable.append(c)

        return ftavailable

    def getParttimeCouples(self, mtg):

        available = []
        couples = Couple.objects.filter(fulltime = False,blockcouple=True)
        for c in couples:
            male_av = Availability.objects.get(meeting = mtg,player = c.male)
            female_av = Availability.objects.get(meeting = mtg,player = c.female)
            if male_av.available and female_av.available:
                available.append(c)

        return available

    def getCouplePlayStats(self,season,couples):
        # Organize by # of plays
        coupleInfo = {}

        meetings = Meetings.objects.filter(season=season,date__lte = datetime.date.today())

        for c in couples:
            cid = c.id

            cinfo = {
                'couple'    : c,
                'plays'     : {
                    'he' : 0,
                    'she' : 0,
                    'they' :0
                }
            }
            coupleInfo[cid] = cinfo
            for m in meetings:
                he = len(Schedule.objects.filter(meeting=m,player=c.male))
                she = len(Schedule.objects.filter(meeting=m,player=c.female))
                if he and she:
                    cinfo['plays']['they'] += 1
                elif he:
                    cinfo['plays']['he'] += 1
                elif she:
                    cinfo['plays']['she'] += 1

        return coupleInfo

    def getNextGroup(self):
        season = self.currentSeason()
        mtg = self.nextMeeting(season)

        needed = 6
        group = []

        ft = self.getFulltimeCouples(mtg)
        if ft:
            for f in ft:
                group.append(f)
                needed -= 1

        pt = self.getParttimeCouples(mtg)

        stats = self.getCouplePlayStats(season,pt)

        def neverPlayed(ci):
            p = ci['plays']
            return p['he'] == p['she'] == p['they'] == 0

        haveNotPlayed = []
        havePlayed = []
        for cid,info in stats.iteritems():
            if neverPlayed(info):
                haveNotPlayed.append(info)
            else:
                havePlayed.append(info)


        # Sort these randomly
        random.shuffle(haveNotPlayed)
        while len(haveNotPlayed) > 0 and needed > 0:
            ci = haveNotPlayed.pop()
            group.append(ci['couple'])
            needed -= 1

        # Sort these by least # of plays.

        def sumPlays(p):
            return p['he'] + p['she'] + p['they']

        def sortPlays(a,b):
            pa = a['plays']
            pb = b['plays']

            tpa = sumPlays(pa)
            tpb = sumPlays(pb)

            if tpa < tpb:
                return -1
            elif tpa > tpb:
                return 1

            return 0


        havePlayed = sorted(havePlayed,sortPlays)
        while len(havePlayed) > 0 and needed > 0:
            ci = havePlayed.pop()
            group.append(ci['couple'])
            needed -= 1


        print("Done")

        return group


    def addCouplesToSchedule(self,couples):

        season = self.currentSeason()
        mtg = self.nextMeeting(season)

        # Clear any existing one first.
        Schedule.objects.filter(meeting=mtg).delete()

        for cpl in couples:
            sm = Schedule.objects.create(
                meeting = mtg,
                player = cpl.male,
                issub = False
            )
            sm.save()

            sh = Schedule.objects.create(
                meeting = mtg,
                player = cpl.female,
                issub = False
            )
            sh.save()


def main():

    tb = Scheduler()

    group = tb.getNextGroup()

    tb.addCouplesToSchedule(group)

    print("Cool")



if __name__ == '__main__':
    main()
