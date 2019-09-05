import datetime

from django.test import TestCase, tag
from django.http import HttpRequest
from unittest import mock
from collections import namedtuple

from api.blockschedule import SubsView
from blockdb.models import (
    Season, Meeting, SeasonPlayer,
    PlayerAvailability
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
class TestBlockSchedule(TestCase):

    def setUp(self):
        self.guys = [GuyPlayerFactory() for g in range(8)]
        self.girls = [GirlPlayerFactory() for g in range(8)]
        self.season = MutedSeasonFactory()
        self.meetings = [MutedMeetingFactory() for m in range(16)]
        self.splayers = [SeasonPlayerFactory() for m in range(len(self.guys) + len(self.girls))]
        for player in self.guys + self.girls:
            PlayerAvailabilityFactory(season=self.season, player=player)

        for mtg in self.meetings:
            # Schedule all players to each meeting
            for idx, player in enumerate(self.guys):
                ScheduleFactory(meeting=mtg, player=player, partner=self.girls[idx])
            for idx, player in enumerate(self.girls):
                ScheduleFactory(meeting=mtg, player=player, partner=self.guys[idx])

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

    def test_sub_list(self):
        self.assertEqual(0, 1, 'Force a TDD failure')

    def test_build_meetings(self):
        self.assertEqual(1, Season.objects.all().count(), "Should have had 16 meetings")
        self.assertEqual(16, Meeting.objects.all().count(), "Should have had 16 meetings")
        self.assertEqual(16, SeasonPlayer.objects.all().count())
        avlist = PlayerAvailability.objects.all()
        for av in avlist:
            self.assertEqual(len(av.available), 16, 'Expected availability to have 16 items')

    def test_block_players_get(self):
        pass

    def test_block_players_post(self):
        pass

    def test_block_dates_query(self):
        pass

    def test_block_schedule_query(self):
        pass

    def test_block_schedule_update(self):
        pass

    def test_block_schedule_delete(self):
        pass
