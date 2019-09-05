import os
import re
import random
from collections import defaultdict
import textwrap

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, F
from django.db import connection

from blockdb.models import PlayerAvailability, Meeting, Couple, Schedule, Player, SeasonPlayer
from api.apiutils import get_current_season, get_next_meeting, get_meeting_for_date


class Scheduler(object):
    def __init__(self):
        pass

    def isPlayerAvailable(self, mtg, player):
        """
        Return True if this player is available on the meeting date.
        """
        meetings = Meeting.objects.filter(season=mtg.season).order_by('date').values_list('date', flat=True)
        mtg_index = list(meetings).index(mtg.date)
        av = PlayerAvailability.objects.get_for_season_player(seasion=mtg.season, player=player)
        return av.available[mtg_index]

    def isCoupleAvailable(self, mtg, couple):
        """
        Check if both members of the given couple are available.
        """

        return self.isPlayerAvailable(mtg, couple.male) \
               and self.isPlayerAvailable(mtg, couple.female)

    def getAvailableCouples(self, season, mtg, fulltime=True):
        couples = Couple.objects.filter(
            season=season, fulltime=fulltime, blockcouple=True)

        availableCouples = [c for c in couples if self.isCoupleAvailable(mtg, c)]

        return availableCouples

    def getCouplePlayStats(self, season, couples):
        # Organize by # of plays
        coupleInfo = {}

        meetings = Meeting.objects.filter(season=season)

        scheduled_meetings = Schedule.objects.filter(meeting__in=meetings)

        for c in couples:
            cid = c.id

            cinfo = {
                'couple': c,
                'plays': {
                    'he': 0,
                    'she': 0,
                    'they': 0,
                    'total': 0
                },
                'weight': 0.0
            }
            coupleInfo[c.name] = cinfo

            either = list(
                scheduled_meetings.filter(Q(player=c.male) | Q(player=c.female)).values('meeting_id', 'player'))

            he = Schedule.objects.filter(meeting__in=meetings, player=c.male).count()
            she = Schedule.objects.filter(meeting__in=meetings, player=c.female).count()

            meeting_sum = defaultdict(int)

            cp = cinfo['plays']
            cp_he = cp['he']
            cp_she = cp['she']
            cp_they = cp['they']

            for e in either:
                mtgid = e.get('meeting_id')
                playerid = e.get('player')
                if playerid == c.male.pk:
                    cp_he += 1
                    meeting_sum[mtgid] += 1
                elif playerid == c.female.pk:
                    cp_she += 1
                    meeting_sum[mtgid] += 1

            cp_they = sum(1 for x in meeting_sum.values() if x == 2)
            cp_he -= cp_they
            cp_she -= cp_they

            cinfo['weight'] = cp_they + cp_he * 0.5 + cp_she * 0.5
            cinfo['plays']['total'] = cp_they + cp_he + cp_she

        return coupleInfo

    def getNextGroup(self, date=None):
        """
        Get the next group of players.

        We have different types of players.
        Couples that want to be scheduled together
        Singles that could be scheduled independently.

        TODO: Figure out how to schedule these fairly.
        """

        season = get_current_season()

        if not season:
            print("No current season configured")
            return None

        if date:
            mtg = get_meeting_for_date(date)
        else:
            mtg = get_next_meeting(season)
        if mtg:
            print("Scheduling for date:%s" % mtg.date)

        needed = season.courts * 2
        group = []

        ft = self.getAvailableCouples(season, mtg, fulltime=True)
        if ft:
            for f in ft:
                group.append(f)
                needed -= 1

        pt = self.getAvailableCouples(season, mtg, fulltime=False)

        stats = self.getCouplePlayStats(season, pt)

        numberOfPlaysMap = {}
        maxNumberOfPlays = 0
        for info in iter(stats.values()):
            nplays = info['plays']['total']
            a = numberOfPlaysMap.setdefault(nplays, [])

            a.append(info)
            maxNumberOfPlays = max(maxNumberOfPlays, nplays)

        for i in range(0, maxNumberOfPlays + 1):
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

    def sortShuffle(self, cinfo):
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

        for weight in sorted(weights.keys(), reverse=True):
            couples = [c for c in cinfo if c['weight'] == weight]
            random.shuffle(couples)
            cinfosortedshuffled.extend(couples)

        return cinfosortedshuffled

    def addCouplesToSchedule(self, date, couples):

        mtg = get_meeting_for_date(date)

        # Clear any existing one first.
        Schedule.objects.filter(meeting=mtg).delete()

        for cpl in couples:
            sm = Schedule.objects.create(
                meeting=mtg,
                player=cpl.male,
                issub=False,
                verified=False,
                partner=cpl.female
            )
            sm.save()

            sh = Schedule.objects.create(
                meeting=mtg,
                player=cpl.female,
                issub=False,
                verified=False,
                partner=cpl.male
            )
            sh.save()

    def removeAllCouplesFromSchedule(self, date):
        """
        Remove all couples from the given date.
        """
        mtg = get_meeting_for_date(date)

        # Clear any existing one first.
        Schedule.objects.filter(meeting=mtg).delete()

    def getPartnerId(self, player):

        if player.gender == 'f':
            c = Couple.objects.filter(female=player)
            if len(c):
                return c[0].male
        else:
            c = Couple.objects.filter(male=player)
            if len(c):
                return c[0].female

        return None

    def _mkData(self, player):
        if player is not None:
            return {
                'name': player.name,
                'id': player.id,
                'ntrp': player.ntrp,
                'untrp': player.microntrp,
            }
        return {'name': '----'}


    def _queryScheduledPlayers(self, mtg):
        """
        Call the stored procedure that does a low-level complex
        full outer join of our players.
        """
        scheduled_players = Schedule.objects.filter(meeting=mtg)
        guys = scheduled_players.filter(player__gender='M')
        gals = scheduled_players.filter(player__gender='F')

        data = [
            {
                'guy': self._mkData(guy.player),
                'gal': self._mkData(guy.partner)
            } for guy in guys
        ]

        # cursor = connection.cursor()
        #
        # cursor.execute("call scheduled_players({});".format(mtg.pk))
        #
        # desc = cursor.description
        # columns = [d[0] for d in desc]
        # rows = cursor.fetchall()
        #
        # data = [dict(zip(columns, r)) for r in rows]

        return data

    def querySchedule(self, date=None):
        """
        Query the schedule of players for the given date.
        """
        mtg = get_meeting_for_date(date)

        if mtg is None:
            return {
                'guys': [],
                'gals': [],
                'couples': []
            }
        
        season = get_current_season()
        num_courts = mtg.num_courts

        data = {}
        if mtg:
            data = {'date': mtg.date}

            guys = []
            gals = []
            couples = []

            results = self._queryScheduledPlayers(mtg)
            for result in results:
                couple = {
                    'guy': {'name': '----'},
                    'gal': {'name': '----'}
                }
                if result.get('guy'):
                    guy = result.get('guy')
                    partner = result.get('gal')
                    g = {
                        'name': guy.get('name'),
                        'id': guy.get('id'),
                        'ntrp': guy.get('ntrp'),
                        'untrp': guy.get('untrp'),
                        'gender': 'm',
                        'partner': result.get('gal'),
                        'partnername': result.get('gal') or '----'
                    }
                    guys.append(g)
                    couple['guy'] = g
                if result.get('gal'):
                    gal = result.get('gal')
                    g = {
                        'name': gal.get('name'),
                        'id': gal.get('id'),
                        'ntrp': gal.get('ntrp'),
                        'untrp': gal.get('untrp'),
                        'gender': 'f',
                        'partner': result.get('guy'),
                        'partnername': result.get('guy') or '----'
                    }
                    gals.append(g)
                    couple['gal'] = g

                couples.append(couple)

            while len(couples) < num_courts*2:
                couples.append({
                    'guy': {'name': '----'},
                    'gal': {'name': '----'}
                })

            data['guys'] = guys
            data['gals'] = gals
            data['couples'] = couples
        else:
            data['date'] = "Invalid"
            data['mtg'] = {'error': 'Could not determine meeting.'}

        return data

    def _addToSchedule(self, mtg, player, partner):
        """
        Add a player to the schedule.

        If the player does not have an ID, then skip
        this player.

        If the player has a partner and that ID is valid
        add their partner.
        """

        try:
            player_obj = Player.objects.get(id=player.get('id', -1))
            if partner.get('id', 0):
                partner = Player.objects.get(id=partner.get('id'))
            else:
                partner = None

            sm = Schedule.objects.create(
                meeting=mtg,
                player=player_obj,
                issub=player.get('issub', False),
                verified=player.get('verified', False),
                partner=partner
            )
            sm.save()
        except ObjectDoesNotExist:
            pass

    def updateSchedule(self, date, couples):
        """
        Update the schedule with the given list.
        """
        mtg = get_meeting_for_date(date)

        if mtg:
            data = {'date': mtg.date}

            # Clear any existing one first.
            Schedule.objects.filter(meeting=mtg).delete()

            for cpl in couples:
                try:
                    md = cpl['guy']
                    fd = cpl['gal']
                    self._addToSchedule(mtg, md, fd)
                    self._addToSchedule(mtg, fd, md)

                except:
                    pass

            return "Schedule updated"
        else:
            return "Could not update schedule."

    def getBlockEmailList(self):
        """
        Return a list of all e-mail addresses for block players.
        """
        players = SeasonPlayer.objects.filter(season=get_current_season(), blockmember=True).only('player')
        addresses = []
        for player in players:
            addr = player.player.email
            if ',' in addr:
                alist = [s.strip() for s in re.split(',', addr)]
                addresses.extend(alist)
            else:
                if addr.strip():
                    addresses.append(addr.strip())

        return addresses


def main():
    tb = Scheduler()

    group = tb.getNextGroup()

    tb.addCouplesToSchedule(group)

    print("Cool")


if __name__ == '__main__':
    main()
