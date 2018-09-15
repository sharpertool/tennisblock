from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ObjectDoesNotExist


class BlockSeason(object):

    def __init__(self,
                 season=None,
                 num_courts=3,
                 first_court=1,
                 season_start=None,
                 season_end=None,
                 block_start=None,
                 block_time=None,
                 holdouts=None, **kwargs):
        """
        Pass in the values, and then validate them
        """
        self.season = season
        if num_courts in [2, 3, 4]:
            self.num_courts = num_courts

        if first_court in [1, 6, 9]:
            self.first_court = first_court

        self.season_start = parse(season_start)
        self.season_end = parse(season_end)
        self.block_start = parse(block_start)
        self.block_time = parse(block_time)

        self.holdouts = []
        if holdouts:
            holdouts = holdouts.split(',')
            for holdout in holdouts:
                holdout_date = parse(holdout)
                if self.season_start <= holdout_date <= self.season_end:
                    self.holdouts.append(holdout_date)


class SeasonManager(object):

    def addSeason(self, sobj):
        """
        Add/Update the given season
        """
        from blockdb.models import Season, Meeting

        res = Season.objects.filter(name=sobj.season)
        if res.count() > 0:
            s = res[0]
            s.courts = sobj.num_courts
            s.firstcourt = sobj.first_court
            s.startdate = sobj.season_start
            s.enddate = sobj.season_end
            s.blockstart = sobj.block_start
            s.blocktime = sobj.block_time

            s.save()
        else:
            s = Season.objects.create(
                name=sobj.season,
                courts=sobj.num_courts,
                firstcourt=sobj.first_court,
                startdate=sobj.season_start,
                enddate=sobj.season_end,
                blockstart=sobj.block_start,
                blocktime=sobj.block_time
            )
            s.save()

        current = sobj.block_start
        while current <= sobj.season_end:
            isHoldout = current in sobj.holdouts
            self.create_or_update_mtg(s, current, isHoldout)
            current = current + relativedelta(weeks=+1)

    def addAllCurrentPlayers(self, seasonName):
        """
        This just adds *all* current players as season players. Then, I
        can go in and adjust the players to see who is on a particular block.
        """

        from blockdb.models import Season, SeasonPlayer, Player

        try:
            sobj = Season.objects.get(name=seasonName)
            players = Player.objects.all()

            for player in players:
                try:
                    SeasonPlayer.objects.get(season=sobj, player=player)
                except ObjectDoesNotExist:
                    sp = SeasonPlayer.objects.create(
                        season=sobj,
                        player=player,
                        blockmember=False
                    )
                    sp.save()

        except ObjectDoesNotExist:
            print("Can't udpate players, can't find season")

    def create_or_update_mtg(self, season, date, isHoldout):

        from blockdb.models import Season, Meeting

        try:
            mtg = Meeting.objects.get(season=season, date=date)
            mtg.holdout = isHoldout
            mtg.save()

        except ObjectDoesNotExist:

            mtg = Meeting.objects.create(
                season=season,
                date=date,
                holdout=isHoldout,
                comments=""
            )
            mtg.save()

        return mtg
