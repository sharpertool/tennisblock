from datetime import datetime
import logging
import os
import re
import random
from typing import List
from collections import defaultdict
import logging
import textwrap
import random
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, F, Max
from django.db import connection
from django.utils import timezone

from blockdb.models import PlayerAvailability, Meeting, Couple, Schedule, Player, SeasonPlayer
from api.apiutils import get_current_season, get_next_meeting, get_meeting_for_date
from TBLib.manager import TeamManager

from .serializers import PlayerSerializer

logger = logging.getLogger(__name__)


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
    def generate_schedule(date=None):
        """ Generate a new schedule for the given date, or current date. """

        group = Scheduler.get_next_group(date)
        if group is None:
            return None

        logger.info("Groups:")
        for g in group:
            logger.info("\tHe:%s She:%s" % (g.male.Name(), g.female.Name()))

        mgr = TeamManager()
        mgr.dbTeams.delete_matchup(date)

        Scheduler.add_group_to_schedule(date, group)

        sched = Scheduler.query_schedule(date)
        return sched

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
    def get_available_couples(mtg, fulltime=None,
                              as_singles=None):
        """
        Get a list of couples that are available for this meeting
        if as_singles is none, then ignore that value
        If set to True or False, apply that filter
        """

        flt = Q(season=mtg.season,
                blockcouple=True
                )

        if fulltime is not None:
            flt = flt & Q(fulltime=fulltime)

        if as_singles:
            flt = flt & Q(as_singles=True)

        couples = Couple.objects.filter(flt)

        available_couples = [
            c for c in couples if Scheduler.is_couple_available(mtg, c)]

        return available_couples

    @staticmethod
    def get_available_singles(mtg):
        """
        Get Players that are not part of a couple
        :param mtg:
        :return:
        """
        flt = Q(season=mtg.season, blockmember=True)
        wflt = flt & Q(player__gender='F')
        mflt = flt & Q(player__gender='M')

        men = SeasonPlayer.objects.filter(mflt).exclude(player_id__in=
        Couple.objects.filter(
            season=mtg.season).values_list(
            'male_id', flat=True)
        )
        women = SeasonPlayer.objects.filter(wflt).exclude(player_id__in=
        Couple.objects.filter(
            season=mtg.season).values_list(
            'female_id', flat=True)
        )

        men = [p for p in men if Scheduler.is_player_available(mtg, p.player)]
        women = [p for p in women if Scheduler.is_player_available(mtg, p.player)]

        return men, women

    @staticmethod
    def get_available_players(mtg, fulltime: bool = False):

        flt = Q(season=mtg.season,
                fulltime=fulltime,
                )

        players = SeasonPlayer.objects.filter(flt)

        guys = [p for p in players if p.player.gender == Player.MALE]
        gals = [p for p in players if p.player.gender == Player.FEMALE]

        return guys, gals

    @staticmethod
    def get_plays_by_player(season, players: List[Player]):
        """
        Return the count of plays for each player, by id
        :param players:
        :return:
        """
        flt = Q(meeting__season=season,
                     meeting__date__lt=datetime.now(),
                     player__in=players
                     )

        query = Schedule.objects.filter(flt).order_by('player')
        query = query.values('player').annotate(plays=Count('player'))

        players_by_plays = defaultdict(list)
        played_players = set()
        for q in query:
            player_id = q['player']
            played_players.add(player_id)
            plays = q['plays']
            players_by_plays[plays].append(player_id)

        for player in players:
            if player.id not in played_players:
                players_by_plays[0].append(player.id)

        return players_by_plays, played_players

    @staticmethod
    def order_players(*,
                      couples: List[Couple],
                      men: List[SeasonPlayer],
                      women: List[SeasonPlayer]):

        season = get_current_season()

        couple_players = [c.male for c in couples] + [c.female for c in couples]

        all_players = [p.player for p in men + women]+couple_players

        couple_players_by_plays, couple_played_players = Scheduler.get_plays_by_player(season, couple_players)
        players_by_plays, played_players = Scheduler.get_plays_by_player(season, [p.player for p in men + women])

        return couple_players_by_plays, players_by_plays

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
            meeting__season=season,
            meeting__date__lt=datetime.now()
        ).order_by(
            'meeting__date'
        ).values('meeting').annotate(f=f).annotate(m=m)

        they = 0
        he = 0
        she = 0
        either = 0

        for stat in stats:
            f = stat.get('f')
            m = stat.get('m')
            if f or m:
                either += 1
            if f and m:
                they += 1
            if m and not f:
                he += 1
            if f and not m:
                she += 1

        cinfo['he_only'] = he
        cinfo['she_only'] = she
        cinfo['either'] = either
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
    def generate_group(*,
                       needed_men: int,
                       needed_women: int,
                       fulltime_couples: List[Couple],
                       parttime_couples: List[Couple],
                       fulltime_men: List[SeasonPlayer],
                       parttime_men: List[SeasonPlayer],
                       fulltime_women: List[SeasonPlayer],
                       parttime_women: List[SeasonPlayer],
                       ):
        """
        This is where we need to determine who plays.
        We need N=courts*4 players, generally N/2 men and N/2 women

        We need fulltime couples and fulltime singles first.
        Then we need to weight singles and couples equally to fill in the rest.

        We need to keep track of couples, men, and women

        Start with FT couples, and ft men/ women
        Even out the men and women from the part-timers.

        Now, we should order the remaining couples, pt men and pt women
        -- this is the hard part.
        We should order by number of plays, and then start with the least.

        :param fulltime_couples:
        :param parttime_couples:
        :param fulltime_men:
        :param parttime_men:
        :param fulltime_women:
        :param parttime_women:
        :return:
        """
        couples = fulltime_couples
        men = fulltime_men
        women = fulltime_women

        needed_men -= (len(men) + len(couples))
        needed_women -= (len(women) + len(couples))

        couple_players_by_plays, players_by_plays = Scheduler.order_players(
            couples=parttime_couples, men=parttime_men, women=parttime_women)

        nplayed = set(couple_players_by_plays.keys()).union(set(players_by_plays.keys()))
        sorted_couples = []
        sorted_men = []
        sorted_women = []
        for n in sorted(nplayed):
            couples = couple_players_by_plays[n]
            players = players_by_plays[n]
            random.shuffle(players)
            random.shuffle(couples)
            sorted_couples.extend(couples)
            sorted_men.extend([p for p in players if p.gender == Player.MALE])
            sorted_women.extend([p for p in players if p.gender == Player.FEMALE])



    @staticmethod
    def get_next_group(date=None):
        """
        Get the next group of players.

        We have different types of players.
        Couples that want to be scheduled together
        Singles that could be scheduled independently.

        TODO: Figure out how to schedule these fairly.
        """

        season = get_current_season()
        ncourts = season.courts

        if not season:
            logger.info("No current season configured")
            return None

        mtg = get_meeting_for_date(date=date)
        if mtg is None:
            logger.error(f"Tried to schedule a date that is not a valid meeting.")
            return None
        logger.info("Scheduling for date:%s" % mtg.date)

        needed = season.courts * 4
        group = []

        men, women = Scheduler.get_available_singles(mtg)
        ft_men = [p for p in men if p.fulltime]
        ft_women = [p for p in women if p.fulltime]
        pt_men = [p for p in men if not p.fulltime]
        pt_women = [p for p in women if not p.fulltime]

        couples = Scheduler.get_available_couples(mtg)
        ft_couples = [c for c in couples if c.fulltime]
        pt_couples = [c for c in couples if not c.fulltime]

        group = Scheduler.generate_group(
            needed_men=season.courts * 2,
            needed_women=season.courts * 2,
            fulltime_couples=ft_couples,
            parttime_couples=pt_couples,
            fulltime_men=ft_men,
            parttime_men=pt_men,
            fulltime_women=ft_women,
            parttime_women=pt_women)
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
    def add_group_to_schedule(date, couples):

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
                logger.info(f"Save for {avail.player.Name()}")
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
