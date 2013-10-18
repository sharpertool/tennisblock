import os
import datetime
os.environ['PYTHONPATH'] = '../../gbrest'
os.environ['DJANGO_SETTINGS_MODULE'] = 'tennisblock_dj.settings.dev'
import random

from django.db import connection
from blockdb.models import *
from api.apiutils import _currentSeason,_nextMeeting,_getMeetingForDate

import tennisblock_dj.settings.dev

class Scheduler(object):

    def __init__(self):
        pass


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

        def _sumPlays(p):
            """
            Sum plays from he, she or they
            """
            return p['he'] + p['she'] + p['they']

        def _weightPlays(p):
            """
            Weight plays from he, she or they
            Give more weight to the he or she, thus giving
            he or she plays higher priority when sorted
            """
            return max(p['he'],p['she'])*1.1 + p['they']

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
            coupleInfo[c.name] = cinfo
            for m in meetings:
                he = len(Schedule.objects.filter(meeting=m,player=c.male))
                she = len(Schedule.objects.filter(meeting=m,player=c.female))
                if he and she:
                    cinfo['plays']['they'] += 1
                elif he:
                    cinfo['plays']['he'] += 1
                elif she:
                    cinfo['plays']['she'] += 1

                cinfo['weight'] = _weightPlays(cinfo['plays'])
                cinfo['plays']['total'] = _sumPlays(cinfo['plays'])

        return coupleInfo

    def getNextGroup(self):
        """
        Get the next group of players.
        """

        season = _currentSeason
        mtg = _nextMeeting(season)
        if mtg:
            print("Scheduling for date:%s" % mtg.date)

        needed = 6
        group = []

        ft = self.getFulltimeCouples(mtg)
        if ft:
            for f in ft:
                group.append(f)
                needed -= 1

        pt = self.getParttimeCouples(mtg)

        stats = self.getCouplePlayStats(season,pt)

        numberOfPlaysMap = {}
        maxNumberOfPlays = 0
        for info in stats.itervalues():
            nplays = info['plays']['total']
            a = numberOfPlaysMap.get(nplays)
            if not a:
                a = []
                numberOfPlaysMap[nplays] = a

            a.append(info)
            maxNumberOfPlays = max(maxNumberOfPlays,nplays)

        for i in range(0,maxNumberOfPlays+1):
            cinfo = numberOfPlaysMap.get(i)
            if cinfo:
                cinfo = self.sortShuffle(cinfo)

                while len(cinfo) and needed > 0:
                    info = cinfo.pop(0)
                    group.append(info['couple'])
                    needed -= 1

            if needed == 0:
                break


        # Should have a full block now..
        return group

    def sortShuffle(self,cinfo):
        """
        Sort and shuffle the list of couples.

        These will be list of couples with equal numbers of total
        plays, but I'd like to further sub-divide them with the goal
        that if he or she only has played, then that couple has 'priority'
        over couples where both have played.

        """
        weights = {}
        for c in cinfo:
            weights[c['weight']] = 1

        cinfosortedshuffled = []

        for weight in sorted(weights.iterkeys(),reverse=True):
            couples = [c for c in cinfo if c['weight'] == weight]
            random.shuffle(couples)
            cinfosortedshuffled.extend(couples)

        return cinfosortedshuffled


    def addCouplesToSchedule(self,date,couples):

        mtg = _getMeetingForDate(date)

        # Clear any existing one first.
        Schedule.objects.filter(meeting=mtg).delete()

        for cpl in couples:
            sm = Schedule.objects.create(
                meeting = mtg,
                player = cpl.male,
                issub = False,
                verified=False,
                partner=cpl.female
            )
            sm.save()

            sh = Schedule.objects.create(
                meeting = mtg,
                player = cpl.female,
                issub = False,
                verified=False,
                partner=cpl.male
            )
            sh.save()

    def getParnerId(self,player):

        if player.gender == 'f':
            c = Couple.objects.filter(female=player)
            if len(c):
                return c[0].male
        else:
            c = Couple.objects.filter(male=player)
            if len(c):
                return c[0].female

        return None

    def querySchedule(self,date=None):
        """
        Query the schedule of players for the given date.
        """
        mtg = _getMeetingForDate(date)

        data = {}
        if mtg:
            data = {'date' : mtg.date}

            guys = []
            gals = []

            schedulePlayers = Schedule.objects.filter(meeting=mtg)
            for sch in schedulePlayers:
                player = sch.player
                if sch.partner:
                    partner = sch.partner
                else:
                    partner = self.getParnerId(player)
                s = {
                    'name' : player.Name(),
                    'id'   : player.id,
                    'ntrp' : player.ntrp,
                    'untrp': player.microntrp,
                    'verify': sch.verified,
                    'issub' : sch.issub
                }
                if partner:
                    s['partner'] = partner.id
                    s['parntername'] = partner.Name()
                else:
                    s['partner'] = None
                    s['parntername'] = ''

                if player.gender == 'F':
                    gals.append(s)
                else:
                    guys.append(s)

            data['guys'] = guys
            data['gals'] = gals
        else:
            data['date'] = "Invalid"
            data['mtg'] = {'error' : 'Could not determine meeting.'}

        return data
    def updateSchedule(selfself,date,guys,gals):
        """
        Update the schedule with the given list.
        """
        mtg = _getMeetingForDate(date)

        if mtg:
            data = {'date' : mtg.date}

            playersById = {}
            for g in guys:
                playersById[g['id']] = g
            for g in gals:
                playersById[g['id']] = g

            schedulePlayers = Schedule.objects.filter(meeting=mtg)
            for sch in schedulePlayers:
                player = sch.player

                if playersById.has_key(player.id):
                    # Match
                    del playersById[player.id]
                else:
                    sch.delete()

            for id in playersById.iterkeys():
                player = Player.objects.get(id=id)
                Schedule.objects.create(
                    meeting=mtg,
                    player=player,
                    issub=True,
                    verified=False
                )

            return "Schedule updated"
        else:
            return "Could not update schedule."



def main():

    tb = Scheduler()

    group = tb.getNextGroup()

    tb.addCouplesToSchedule(group)

    print("Cool")



if __name__ == '__main__':
    main()
