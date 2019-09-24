import os
import re
import random
from collections import defaultdict
import textwrap

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, F
from django.db import connection
from django.utils import timezone

from blockdb.models import PlayerAvailability, Meeting, Couple, Schedule, Player, SeasonPlayer
from api.apiutils import get_current_season, get_next_meeting, get_meeting_for_date


def reset_availability_arrays(date=None):
    """ Reset availability arrays for given meeting date,
    or all in current season if date is empty """

    if date:
        meetings = [get_meeting_for_date(date)]
    else:
        season = get_current_season()
        meetings = Meeting.objects.filter(season=season)

    scheduler = Scheduler()
    for meeting in meetings:
        scheduler.update_scheduled_for_players(meeting)


class Scheduler(object):
    def __init__(self):
        pass

    def is_player_available(self, mtg, player):
        """
        Return True if this player is available on the meeting date.
        """
        mtg_index = mtg.meeting_index
        av = PlayerAvailability.objects.get_for_season_player(season=mtg.season, player=player)
        return av.available[mtg_index]

    def is_couple_available(self, mtg, couple):
        """
        Check if both members of the given couple are available.
        """

        return all([self.is_player_available(mtg, couple.male),
                    self.is_player_available(mtg, couple.female)])

    def get_available_couples(self, mtg, fulltime=True,
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
            c for c in couples if self.is_couple_available(mtg, c)]

        return availableCouples

    def get_available_singles(self, mtg):
        couples = Couple.objects.filter(
            season=mtg.season,
            as_singles=True,
            blockcouple=True)

        guys = []
        girls = []
        for couple in couples:
            if self.is_player_available(mtg, couple.male):
                guys.append(couple.male)
            if self.is_player_available(mtg, couple.female):
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

    def get_couple_stats(self, season, couples):
        """ Organize by # of plays """

        info = {}
        for couple in couples:
            couple_info = self.calc_play_stats_for_couple(
                season=season,
                couple=couple,
            )
            info[couple.name] = couple_info

        return info

    def get_singles_stats(self, season, players):
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

    def get_next_group(self, date=None, with_singles=None):
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

        ft = self.get_available_couples(mtg)
        if ft:
            for f in ft:
                group.append(f)
                needed -= 1

        guys, girls = self.get_available_singles(mtg)

        as_singles = None
        if with_singles:
            as_singles = False
        pt = self.get_available_couples(mtg,
                                        fulltime=False,
                                        as_singles=as_singles
                                        )

        stats = self.get_couple_stats(season, pt)

        info_by_plays = self.sort_info(stats)
        plays = sorted(info_by_plays.keys())
        for i in plays:
            info_data = info_by_plays.get(i)
            if info_data:
                info_data = self.sort_shuffle(info_data)

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

    def add_couples_to_schedule(self, date, couples):

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

        self.update_scheduled_for_players(mtg)

    def remove_all_couples_from_schedule(self, date):
        """
        Remove all couples from the given date.
        """
        mtg = get_meeting_for_date(date)

        # Clear any existing one first.
        Schedule.objects.filter(meeting=mtg).delete()
        self.update_scheduled_for_players(mtg)

    def get_partner_id(self, player):

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

    def _query_scheduled_players(self, mtg):
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

    def query_schedule(self, date=None):
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

            results = self._query_scheduled_players(mtg)
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

            while len(couples) < num_courts * 2:
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

    def update_schedule_players(self, meeting, couples):

        schedule_player_ids = []
        for cpl in couples:
            md = cpl['guy']
            fd = cpl['gal']
            msub, fsub = md.get('issub', False), fd.get('issub', False)
            mverified, fverified = md.get('verified', False), fd.get('verified', False)
            player, partner = self.get_players(md, fd)

            if player:
                self.add_or_update_schedule(meeting, player, partner,
                                            is_sub=msub,
                                            verified=mverified
                                            )
                schedule_player_ids.append(player.id)
            if partner:
                self.add_or_update_schedule(meeting, partner, player,
                                            is_sub=fsub,
                                            verified=fverified
                                            )
                schedule_player_ids.append(partner.id)

        # Delete any players that were scheduled.
        Schedule.objects.filter(meeting=meeting).filter(
            ~Q(player_id__in=schedule_player_ids)).delete()

        # Update the player availability arrays.
        self.update_scheduled_for_players(meeting)

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
    def update_played_for_players(self,  meeting, scheduled_pks=None):
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

    def get_players(self, player, partner):
        """ Get the player and partner objects from dict """

        try:
            player_obj = Player.objects.get(id=player.get('id'))
        except Player.DoesNotExist:
            player_obj = None

        try:
            partner_obj = Player.objects.get(id=partner.get('id'))
        except Player.DoesNotExist:
            partner_obj = None

        return player_obj, partner_obj

    def add_or_update_schedule(self, meeting, player, partner,
                               is_sub=False, verified=False):
        """
        Add or update the schedule
        Retain the existing schedule object for a player so that
        we can retain the schedule verification

        The caller is simplified, so it may send a None as player,
        which we just ignore

        """
        if player is None:
            return

        try:
            schedule = Schedule.objects.get(
                meeting=meeting, player=player
            )
            changed = False
            if schedule.partner != partner:
                schedule.partner = partner
                changed = True
            if schedule.issub != is_sub:
                schedule.issub = is_sub
                changed = True

            if changed:
                schedule.save()
                return True

        except Schedule.DoesNotExist:
            schedule = Schedule(
                meeting=meeting,
                player=player,
                issub=is_sub,
                verified=verified,
                partner=partner
            )
            schedule.save()
            return True

        return False

    def _add_to_schedule(self, mtg, player, partner):
        """
        Add a player to the schedule.

        If the player does not have an ID, then skip
        this player.

        If the player has a partner and that ID is valid
        add their partner.
        """

        try:
            player_obj = Player.objects.get(id=player.get('id'))
            if partner.get('id') is not None:
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

    def update_schedule(self, date, couples):
        """
        Update the schedule with the given list.
        """
        mtg = get_meeting_for_date(date)

        if mtg:
            self.update_schedule_players(mtg, couples)
            return "Schedule updated"
        else:
            return "Could not update schedule."

    def get_block_email_list(self):
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

    def get_notify_email_lists(self, date=None):
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


def main():
    tb = Scheduler()

    group = tb.get_next_group()

    tb.add_couples_to_schedule(group)

    print("Cool")


if __name__ == '__main__':
    main()
