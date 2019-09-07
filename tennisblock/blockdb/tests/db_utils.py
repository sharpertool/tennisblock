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

    @staticmethod
    def staticCoreSetup():
        guys = [GuyPlayerFactory() for g in range(8)]
        girls = [GirlPlayerFactory() for g in range(8)]
        season = MutedSeasonFactory()
        season.ensure_meetings_exist()
        meetings = season.meetings

        return guys, girls, season, meetings

    @staticmethod
    def staticPlayersSetup(season, girls, guys):
        splayers = [SeasonPlayerFactory(season=season, player=p)
                         for p in guys + girls]
        for player in guys + girls:
            PlayerAvailabilityFactory(season=season, player=player)

        return splayers

    @staticmethod
    def static_couples_setup(season, girls, guys):
        couples = []
        for i, guy in enumerate(guys):
            gal = girls[i]
            couple = Couple(
                season=season,
                name="bogus",
                male=guy,
                female=gal,
                fulltime=False,
                blockcouple=True,
                as_singles=False,
            )
            couples.append(couple)

        return couples

    @staticmethod
    def static_meeting_setup(meetings, girls, guys):
        for mtg in meetings:
            # Schedule all players to each meeting
            for idx, player in enumerate(guys):
                ScheduleFactory(
                    meeting=mtg, player=player, partner=girls[idx])
            for idx, player in enumerate(girls):
                ScheduleFactory(
                    meeting=mtg, player=player, partner=guys[idx])

    @staticmethod
    def static_match_setup(meetings, girls, guys):
        for mtg in meetings:
            for set in range(3):
                for court in range(4):
                    guys = guys[2 * court:2 * court + 2]
                    gals = girls[2 * court:2 * court + 2]
                    MatchupFactory(
                        meeting=mtg,
                        set=set,
                        court=court,
                        team1_p1=guys[0],
                        team1_p2=gals[0],
                        team2_p1=guys[1],
                        team2_p2=gals[1],
                    )

    def coreSetup(self):
        results = self.staticCoreSetup()
        [self.guys, self.girls, self.season, self.meetings] = results

    def playersSetup(self):
        self.splayers = self.staticPlayersSetup(
            self.season, self.girls, self.guys
        )

    def couples_setup(self):
        self.couples = self.static_couples_setup(
            self.season, self.girls, self.guys)

    def meetingSetup(self):
        self.static_meeting_setup(
            self.season,
            self.girls,
            self.guys)

    def matchupSetup(self):
        self.static_match_setup()

    def allSetup(self):
        self.coreSetup()
        self.playersSetup()
        self.meetingSetup()
        self.matchupSetup()
