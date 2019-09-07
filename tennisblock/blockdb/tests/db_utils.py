import datetime

from django.test import TestCase, tag
from django.http import HttpRequest
from unittest import mock
from collections import namedtuple

from api.blockschedule import SubsView
from blockdb.models import (
    Season, Meeting, SeasonPlayer,
    PlayerAvailability,
    Couple
)
from blockdb.factories import (
    GuyPlayerFactory, GirlPlayerFactory,
    SeasonFactory, MutedSeasonFactory,
    MeetingFactory, MutedMeetingFactory,
    SeasonPlayerFactory,
    PlayerAvailabilityFactory,
    ScheduleFactory,
    MatchupFactory,
)


@tag('medium')
class BlockDBTestBase(TestCase):

    def coreSetup(self):
        self.guys = [GuyPlayerFactory() for g in range(8)]
        self.girls = [GirlPlayerFactory() for g in range(8)]
        self.season = MutedSeasonFactory()
        self.season.ensure_meetings_exist()
        self.meetings = self.season.meetings

    def playersSetup(self):
        self.splayers = [SeasonPlayerFactory(season=self.season, player=p)
                         for p in self.guys + self.girls]
        for player in self.guys + self.girls:
            PlayerAvailabilityFactory(season=self.season, player=player)

    def couples_setup(self):
        for i, guy in enumerate(self.guys):
            gal = self.girls[i]
            couple = Couple(
                season=self.season,
                name="bogus",
                male=guy,
                female=gal,
                fulltime=False,
                blockcouple=True,
                as_singles=False,
            )

    def meetingSetup(self):
        for mtg in self.meetings:
            # Schedule all players to each meeting
            for idx, player in enumerate(self.guys):
                ScheduleFactory(
                    meeting=mtg, player=player, partner=self.girls[idx])
            for idx, player in enumerate(self.girls):
                ScheduleFactory(
                    meeting=mtg, player=player, partner=self.guys[idx])

    def matchupSetup(self):
        for mtg in self.meetings:
            for set in range(3):
                for court in range(4):
                    guys = self.guys[2 * court:2 * court + 2]
                    gals = self.girls[2 * court:2 * court + 2]
                    MatchupFactory(
                        meeting=mtg,
                        set=set,
                        court=court,
                        team1_p1=guys[0],
                        team1_p2=gals[0],
                        team2_p1=guys[1],
                        team2_p2=gals[1],
                    )

    def allSetup(self):
        self.coreSetup()
        self.playersSetup()
        self.meetingSetup()
        self.matchupSetup()
