from datetime import datetime
import os
import re
import random
from collections import defaultdict
import textwrap

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, F, Max
from django.db import connection
from django.utils import timezone

from blockdb.models import PlayerAvailability, Meeting, Couple, Schedule, Player, SeasonPlayer
from api.apiutils import get_current_season, get_next_meeting, get_meeting_for_date

from .serializers import PlayerSerializer


def reset_availability_arrays(date=None):
    """ Reset availability arrays for given meeting date,
    or all in current season if date is empty """

    if date:
        meetings = [get_meeting_for_date(date)]
    else:
        season = get_current_season()
        meetings = Meeting.objects.filter(season=season).order_by('date')

    scheduler = Scheduler()
    for meeting in meetings:
        scheduler.update_scheduled_for_players(meeting)


def update_availability_played_arrays():
    """ Set played to true for all past dates where scheduled is true """

    season = get_current_season()

    scheduler = Scheduler()
    scheduler.update_played_for_season(season)


class Scheduler(object):

    @staticmethod
    def is_player_available(mtg, player):
        """
        Return True if this player is available on the meeting date.
        """
        mtg_index = mtg.meeting_index
        av = PlayerAvailability.objects.get_for_season_player(season=mtg.season, player=player)
        return av.available[mtg_index]

    @staticmethod
    def is_couple_available(mtg, couple):
        """
        Check if both members of the given couple are available.
        """

        return all([Scheduler.is_player_available(mtg, couple.male),
                    Scheduler.is_player_available(mtg, couple.female)])

    @staticmethod
    def get_available_couples(mtg, fulltime=True,
                              as_singles=None):
        """
        Get a list of couples that are available for this meeting
        if as_singles is none, then ignore that value
        If set to True or False, apply that filter
        """

        flt = Q(season=mtg.season,
                fulltime=fulltime,
                blockcouple=True
                )
        singles_flt = Q()
        if as_singles:
            singles_flt = Q(as_singles=True)

        couples = Couple.objects.filter(
            flt & singles_flt
        )

        availableCouples = [
            c for c in couples if Scheduler.is_couple_available(mtg, c)]

        return availableCouples

    @staticmethod
    def get_available_singles(mtg):
        couples = Couple.objects.filter(
            season=mtg.season,
            as_singles=True,
            blockcouple=True)

        guys = []
        girls = []
        for couple in couples:
            if Scheduler.is_player_available(mtg, couple.male):
                guys.append(couple.male)
            if Scheduler.is_player_available(mtg, couple.female):
                girls.append(couple.female)

        return guys, girls

    @staticmethod
    def calc_play_stats_for_couple(season=None, couple=None):
        cinfo = {
            'couple': couple,
            'total_plays': 0,
            'he_only': 0,
            'she_only': 0,
            'weight': 0.0
        }

        f = Count('player', filter=Q(player__gender='F'))
        m = Count('player', filter=Q(player__gender='M'))

        stats = Schedule.objects.filter(
            meeting__season=season
        ).order_by(
            'meeting__date'
        ).values('meeting').annotate(f=f).annotate(m=m)

        they = 0
        he = 0
        she = 0

        for stat in stats:
            f = stat.get('f')
            m = stat.get('m')
            if f and m:
                they += 1
            if m and not f:
                he += 1
            if f and not m:
                she += 1

        cinfo['he_only'] = he
        cinfo['she_only'] = she
        cinfo['total_plays'] = she + he + they
        cinfo['weight'] = they + he * 0.5 + she * 0.5

        return cinfo

    @staticmethod
    def get_couple_stats(season, couples):
        """ Organize by # of plays """

        info = {}
        for couple in couples:
            couple_info = Scheduler.calc_play_stats_for_couple(
                season=season,
                couple=couple,
            )
            info[couple.name] = couple_info

        return info

    @staticmethod
    def get_singles_stats(season, players):
        """
        Return stats for how many times the player has played
        """
        for player in players:
            played = Schedule.objects.filter(
                meeting__season=season,
                player=player
            ).count()

        return {}

    @staticmethod
    def sort_info(stats):
        couples_by_plays = {}
        for info in stats.values():
            nplays = info['total_plays']
            a = couples_by_plays.setdefault(nplays, [])
            a.append(info)

        return couples_by_plays

    @staticmethod
    def get_next_group(date=None, with_singles=None):
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

        mtg = get_meeting_for_date(date=date)
        print("Scheduling for date:%s" % mtg.date)

        needed = season.courts * 2
        group = []

        ft = Scheduler.get_available_couples(mtg)
        if ft:
            for f in ft:
                group.append(f)
                needed -= 1

        guys, girls = Scheduler.get_available_singles(mtg)

        as_singles = None
        if with_singles:
            as_singles = False
        pt = Scheduler.get_available_couples(mtg,
                                             fulltime=False,
                                             as_singles=as_singles
                                             )

        stats = Scheduler.get_couple_stats(season, pt)

        info_by_plays = Scheduler.sort_info(stats)
        plays = sorted(info_by_plays.keys())
        for i in plays:
            info_data = info_by_plays.get(i)
            if info_data:
                info_data = Scheduler.sort_shuffle(info_data)

                while len(info_data) and needed > 0:
                    info = info_data.pop(0)
                    group.append(info.get('couple'))
                    needed -= 1

            if needed == 0:
                break

        # Should have a full block now..
        return group

    @staticmethod
    def sort_shuffle(cinfo):
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

    @staticmethod
    def add_couples_to_schedule(date, couples):

        mtg = get_meeting_for_date(date)

        # Clear any existing one first.
        Schedule.objects.filter(meeting=mtg).delete()

        for idx, cpl in enumerate(couples):
            sm = Schedule.objects.create(
                meeting=mtg,
                pair_index=idx,
                player=cpl.male,
                issub=False,
                verified=False,
                partner=cpl.female
            )
            sm.save()

            sh = Schedule.objects.create(
                meeting=mtg,
                pair_index=idx,
                player=cpl.female,
                issub=False,
                verified=False,
                partner=cpl.male
            )
            sh.save()

        Scheduler.update_scheduled_for_players(mtg)

    @staticmethod
    def remove_all_couples_from_schedule(date):
        """
        Remove all couples from the given date.
        """
        mtg = get_meeting_for_date(date)

        # Clear any existing one first.
        Schedule.objects.filter(meeting=mtg).delete()
        Scheduler.update_scheduled_for_players(mtg)

    @staticmethod
    def get_partner_id(player):

        if player.gender == 'F':
            c = Couple.objects.filter(female=player)
            if len(c):
                return c[0].male
        else:
            c = Couple.objects.filter(male=player)
            if len(c):
                return c[0].female

        return None

    @staticmethod
    def _mkData(player):
        if player is not None:
            return {
                'name': player.name,
                'id': player.id,
                'ntrp': player.ntrp,
                'untrp': player.microntrp,
            }
        return {'name': '----'}

    @staticmethod
    def get_couples(mtg):

        couples = Schedule.objects.filter(meeting=mtg).distinct('pair_index').order_by('pair_index')

        clist = []
        for couple in couples:
            g1 = couple.player.gender
            if couple.partner:
                g2 = couple.partner.gender
            else:
                g2 = ' '
            gpair = g1 + g2
            if gpair in ['MF', 'MM', 'FF']:
                clist.append((couple.player.id, couple.partner.id, couple.pair_index))
            elif gpair == 'M ':
                clist.append((couple.player.id, -1, couple.pair_index))
            elif gpair == 'F ':
                clist.append((-1, couple.player.id, couple.pair_index))
            else:  # gpair == 'FM'
                clist.append((couple.partner.id, couple.player.id, couple.pair_index))

        return clist

    @staticmethod
    def _query_scheduled_players(mtg):
        """
        Call the stored procedure that does a low-level complex
        full outer join of our players.
        """
        scheduled = Schedule.objects.filter(meeting=mtg)
        sched_guys = scheduled.filter(player__gender='M')

        guys = Player.objects.filter(id__in=scheduled.filter(
            player__gender='M').values('player__id'))
        gals = Player.objects.filter(id__in=scheduled.filter(
            player__gender='F').values('player__id'))

        data = [
            {
                'guy': Scheduler._mkData(guy.player),
                'gal': Scheduler._mkData(guy.partner),
            } for guy in sched_guys
        ]

        couples = Scheduler.get_couples(mtg)

        return {
            "pairs": data,
            "guys": PlayerSerializer(guys, many=True).data,
            "gals": PlayerSerializer(gals, many=True).data,
            "couples": couples}

    @staticmethod
    def query_schedule(date=None):
        """
        Query the schedule of players for the given date.
        """
        mtg = get_meeting_for_date(date)

        data = {
            'status': 'fail',
            'msg': 'No meeting for date',
            'date': date,
            'num_courts': -1,
            'guys': [],
            'gals': [],
            'couples': []
        }

        if mtg is None:
            return data

        data['date'] = mtg.date
        data['num_courts'] = mtg.num_courts

        guys = []
        gals = []

        results = Scheduler._query_scheduled_players(mtg)
        pairs = results.get('pairs')
        couples = results.get('couples')
        for pair in pairs:
            couple = {
                'guy': {'name': '----'},
                'gal': {'name': '----'}
            }
            if pair.get('guy'):
                guy = pair.get('guy')
                partner = pair.get('gal')
                g = {
                    'name': guy.get('name'),
                    'id': guy.get('id'),
                    'ntrp': guy.get('ntrp'),
                    'untrp': guy.get('untrp'),
                    'gender': 'm',
                    'partner': pair.get('gal'),
                    'partnername': pair.get('gal') or '----'
                }
                guys.append(g)
                couple['guy'] = g
            if pair.get('gal'):
                gal = pair.get('gal')
                g = {
                    'name': gal.get('name'),
                    'id': gal.get('id'),
                    'ntrp': gal.get('ntrp'),
                    'untrp': gal.get('untrp'),
                    'gender': 'f',
                    'partner': pair.get('guy'),
                    'partnername': pair.get('guy') or '----'
                }
                gals.append(g)
                couple['gal'] = g

        data['guys'] = results.get('guys')
        data['gals'] = results.get('gals')
        data['couples'] = couples
        data['status'] = 'success'
        data['msg'] = ''

        return data

    @staticmethod
    def update_schedule_players(meeting, couples):
        """
        Iterate over the couples array, which is an array of tuples, where
        each tuple is (player.id, partner.id, index)

        The index is used to associate the players as a pair.
        Update or create entries for each player/partner pair in the Schedule

        """

        schedule_player_ids = []
        for cpl in couples:
            p1, p2, pair_index = cpl
            player, partner = Scheduler.get_players(p1, p2)

            if player:
                Scheduler.add_or_update_schedule(meeting, player, partner, index=pair_index)
                schedule_player_ids.append(player.id)
            if partner:
                Scheduler.add_or_update_schedule(meeting, partner, player, index=pair_index)
                schedule_player_ids.append(partner.id)

        # Delete any players that were scheduled.
        Schedule.objects.filter(meeting=meeting).filter(
            ~Q(player_id__in=schedule_player_ids)).delete()

        # Update the player availability arrays.
        Scheduler.update_scheduled_for_players(meeting)

    @staticmethod
    def update_scheduled_for_players(meeting, scheduled_pks=None):
        """ Set scheduled PK's to True, others to false """

        is_future = meeting.date > timezone.now().date()
        if scheduled_pks is None:
            scheduled_pks = Schedule.objects.filter(
                meeting=meeting).values_list('player__pk', flat=True)

        idx = meeting.season_index
        scheduled = PlayerAvailability.objects.filter(
            season=meeting.season,
            player_id__in=scheduled_pks)
        for av in scheduled:
            changed = False
            if not av.scheduled[idx]:
                av.scheduled[idx] = True
                changed = True

            if is_future:
                if av.played[idx]:
                    av.played[idx] = False
                    changed = True
            else:
                if not av.played[idx]:
                    av.played[idx] = True
                    changed = True

            if changed:
                av.save()

        unscheduled = PlayerAvailability.objects.filter(
            season=meeting.season).filter(~Q(player_id__in=scheduled_pks))
        for av in unscheduled:
            changed = False
            if av.scheduled[idx]:
                av.scheduled[idx] = False
                changed = True

            if av.played[idx]:
                av.played[idx] = False
                changed = True

            if changed:
                av.save()

    @staticmethod
    def update_played_for_season(season):
        """
        Set played to true if date is past and scheduled is true
        :param season:
        :return:
        """

        availabilities = PlayerAvailability.objects.filter(
            season=season
        )
        past_meetings = Meeting.objects.filter(
            season=season
        ).filter(
            date__lt=datetime.now()
        ).count()

        for avail in availabilities:
            changed = False
            for x in range(past_meetings):
                if (avail.played[x] != avail.scheduled[x]):
                    changed = True
                    avail.played[x] = avail.scheduled[x]

            if changed:
                print(f"Save for {avail.player.Name()}")
                avail.save()


    @staticmethod
    def update_played_for_players(meeting, scheduled_pks=None):
        """ Set played PK's to True, others to false """

        if scheduled_pks is None:
            scheduled_pks = Schedule.objects.filter(
                meeting=meeting).values_list('player__pk', flat=True)

        idx = meeting.season_index
        scheduled = PlayerAvailability.objects.filter(
            season=meeting.season,
            player_id__in=scheduled_pks)
        for av in scheduled:
            if not av.scheduled[idx]:
                av.scheduled[idx] = True
                av.save()

        unscheduled = PlayerAvailability.objects.filter(
            season=meeting.season).fitler(~Q(player_id__in=scheduled_pks))
        for av in unscheduled:
            if av.scheduled[idx]:
                av.scheduled[idx] = False
                av.save()

    @staticmethod
    def get_player_obj(player):
        """ Retrieve the player object with dict or int """
        try:
            if isinstance(player, dict):
                player_obj = Player.objects.get(id=player.get('id'))
            elif isinstance(player, int):
                player_obj = Player.objects.get(id=player)
        except Player.DoesNotExist:
            player_obj = None
        return player_obj

    @staticmethod
    def get_players(player, partner):
        """ Get the player and partner objects from dict """

        player_obj = Scheduler.get_player_obj(player)
        partner_obj = Scheduler.get_player_obj(partner)

        return player_obj, partner_obj

    @staticmethod
    def add_or_update_schedule(meeting, player, partner,
                               is_sub=False, verified=False,
                               index=None):
        """
        Add or update the schedule
        Retain the existing schedule object for a player so that
        we can retain the schedule verification

        The caller is simplified, so it may send a None as player,
        which we just ignore

        """
        if player is None:
            return

        obj, created = Schedule.objects.update_or_create(
            player=player,
            meeting=meeting,
            defaults={
                'issub': is_sub,
                'verified': verified,
                'pair_index': index,
                'partner': partner,
                'confirmation_status': 'U'}
        )

        return created

    @staticmethod
    def update_schedule(date, couples):
        """
        Update the schedule with the given list.
        """
        mtg = get_meeting_for_date(date)

        if mtg:
            Scheduler.update_schedule_players(mtg, couples)
            return "Schedule updated"
        else:
            return "Could not update schedule."

    @staticmethod
    def get_block_email_list():
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

    @staticmethod
    def get_notify_email_lists(date=None):
        """
        Return an email list for scheduled players,
        and a CC list for players that are not scheduled
        but members of the block.
        """

        mtg = get_meeting_for_date(date)
        players = Schedule.objects.filter(meeting=mtg)
        season_players = SeasonPlayer.objects.filter(
            blockmember=True,
            season=mtg.season
        )
        ids = [s.player.id for s in players]
        other_players = season_players.filter(
            ~Q(player__in=ids)
        )
        cc_list = [s.player.user.email
                   for s in other_players]
        email_list = [s.player.user.email
                      for s in players]

        return email_list, cc_list
