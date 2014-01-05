#!/usr/bin/env python

import sys

import os
from os.path import join,expanduser
sys.path.append(expanduser("~/proj/bondiproj/tennisblock"))

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from dateutil.parser import *
from dateutil.relativedelta import *

from types import *

import argparse

class BlockSeason(object):

    def __init__(self,
                        season=None,
                        num_courts=3,
                        first_court=1,
                        season_start=None,
                        season_end=None,
                        block_start=None,
                        block_time=None,
                        holdouts=[],**kwargs):
        """
        Pass in the values, and then validate them
        """
        self.season = season
        if num_courts in [2,3,4]:
            self.num_courts = num_courts

        if first_court in [1,6,9]:
            self.first_court = first_court

        self.season_start = parse(season_start)
        self.season_end = parse(season_end)
        self.block_start = parse(block_start)
        self.block_time = parse(block_time)


        self.holdouts = []
        for ho in holdouts:
            hodate = parse(ho)
            if hodate >= self.season_start and hodate <= self.season_end:
                self.holdouts.append(hodate)

class SeasonManager(object):

    def __init__(self,setting):

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennisblock.settings.%s" % setting)

    def addSeason(self,sobj):
        """
        Add/Update the given season
        """
        from tennisblock.blockdb.models import Season,Meetings

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
                name        = sobj.season,
                courts      = sobj.num_courts,
                firstcourt  = sobj.first_court,
                startdate   = sobj.season_start,
                enddate     = sobj.season_end,
                blockstart  = sobj.block_start,
                blocktime   = sobj.block_time
            )
            s.save()

        current = sobj.block_start
        while current <= sobj.season_end:
            isHoldout = current in sobj.holdouts
            self.create_or_update_mtg(s,current,isHoldout)
            current = current + relativedelta(weeks=+1)

    def addAllCurrentPlayers(self,seasonName):
        """
        This just adds *all* current players as season players. Then, I
        can go in and adjust the players to see who is on a particular block.
        """

        from tennisblock.blockdb.models import Season,SeasonPlayers,Player

        try:
            sobj = Season.objects.get(name=seasonName)
            players = Player.objects.all()

            for player in players:
                try:
                    SeasonPlayers.objects.get(season=sobj,player=player)
                except ObjectDoesNotExist:
                    sp = SeasonPlayers.objects.create(
                        season=sobj,
                        player=player,
                        blockmember=False
                    )
                    sp.save()

        except ObjectDoesNotExist:
            print("Can't udpate players, can't find season")


    def create_or_update_mtg(self,season,date,isHoldout):

        from tennisblock.blockdb.models import Season,Meetings

        try:
            mtg = Meetings.objects.get(season=season,date=date)
            mtg.holdout = isHoldout
            mtg.save()

        except ObjectDoesNotExist:

            mtg = Meetings.objects.create(
                season=season,
                date=date,
                holdout = isHoldout,
                comments=""
            )
            mtg.save()

        return mtg

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("season",help="Name this season, Fall 2013, etc.")
    parser.add_argument("num_courts",type=int,help="Number of courts.")
    parser.add_argument("first_court",type=int,help="Starting court at facility. Assumes linear numbering.")
    parser.add_argument("season_start",help="Date that this block season starts")
    parser.add_argument("season_end",help="Date that this block season ends.")
    parser.add_argument("block_start",help="The date that this block starts. Set the block day")
    parser.add_argument("block_time")

    parser.add_argument("holdouts", nargs="*", help="Holdout dates.")

    parser.add_argument("--setting", default="dev", help="Choose the setting")

    args = parser.parse_args()

    bs = BlockSeason(**vars(args))

    mgr = SeasonManager(args.setting)

    mgr.addSeason(bs)

    mgr.addAllCurrentPlayers(bs.season)


if __name__ == '__main__':
    main()


