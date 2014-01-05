import os
import datetime
os.environ['PYTHONPATH'] = '../../gbrest'
os.environ['DJANGO_SETTINGS_MODULE'] = 'tennisblock_dj.settings.dev'
import random

from tennisblock.blockdb.models import *
from tennisblock.api.apiutils import _currentSeason,_nextMeeting,_getMeetingForDate
from django.core.exceptions import ObjectDoesNotExist


class Scheduler(object):

    def __init__(self):
        pass

    def checkAvailability(self,mtg,male,female):
        """
        Check availability of the given couple.
        If the availability does not exist for that couple, then mark them
        as available.
        """
        maleIsAvailable = True
        femaleIsAvailable = True
        try:
            male_av = Availability.objects.get(meeting = mtg,player = male)
            maleIsAvailable=male_av.available
        except ObjectDoesNotExist:
            Availability.objects.create(meeting = mtg,player = male,available=True).save()

        try:
            female_av = Availability.objects.get(meeting = mtg,player = female)
        except ObjectDoesNotExist:
            Availability.objects.create(meeting = mtg,player = female,available=True).save()

        return maleIsAvailable and femaleIsAvailable

    def getAvailableCoulpes(self,season,mtg,fulltime=True):
        availableCouples = []
        couples = Couple.objects.filter(
            season=season,fulltime = fulltime,blockcouple=True)

        for c in couples:
            if self.checkAvailability(mtg,c.male,c.female):
                availableCouples.append(c)

        return availableCouples

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
                    'they' :0,
                    'total' : 0
                },
                'weight' : 0.0
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

        ft = self.getAvailableCoulpes(season,mtg,fulltime=True)
        if ft:
            for f in ft:
                group.append(f)
                needed -= 1

        pt = self.getAvailableCoulpes(season,mtg,fulltime=False)

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
    def updateSchedule(selfself,date,couples):
        """
        Update the schedule with the given list.
        """
        mtg = _getMeetingForDate(date)

        if mtg:
            data = {'date' : mtg.date}

            playersById = {}
            for c in couples:
                guy = c['currguy']
                playersById[guy['id']] = {
                        'player' : guy,
                        'partner' : c['currgal']
                    }
                gal = c['currgal']
                playersById[gal['id']] = {
                    'player' : gal,
                    'partner' : c['currguy']
                }

            # Clear any existing one first.
            Schedule.objects.filter(meeting=mtg).delete()

            for cpl in couples:
                try:
                    md = cpl['currguy']
                    fd = cpl['currgal']
                    guy = Player.objects.get(id=md['id'])
                    gal = Player.objects.get(id=fd['id'])
                    sm = Schedule.objects.create(
                        meeting = mtg,
                        player = guy,
                        issub = md.get('issub',False),
                        verified=md.get('verified',False),
                        partner=gal
                    )
                    sm.save()

                    sh = Schedule.objects.create(
                        meeting = mtg,
                        player = gal,
                        issub = fd.get('issub',False),
                        verified=fd.get('verified',False),
                        partner=guy
                    )
                    sh.save()
                except:
                    pass

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
