from django.test import TestCase
from django.db import IntegrityError

from blockdb.models import (
    PlayerAvailability,
    Player,
    Couple,
    SeasonPlayer,
    Season,
    Schedule,
)
from TBLib.season import SeasonManager
from TBLib.schedule import Scheduler

from blockdb.tests.db_utils import BlockDBTestBase


class TestAvailability(BlockDBTestBase):

    @classmethod
    def setUpTestData(cls):
        results = cls.staticCoreSetup()
        [cls.guys, cls.girls, cls.season, cls.meetings] = results

    def setUp(self):
        pass

    def test_is_player_available(self):
        """
        Test if a player is available for a given meeting
        """
        sch = Scheduler()

        mtg = self.meetings[0]
        print(f'Meeting index {mtg.meeting_index}')
        player = self.guys[0]
        av = PlayerAvailability.objects.get_for_season_player(
            season=self.season, player=player)

        self.assertTrue(sch.is_player_available(mtg, player))
        av.available[0] = False
        av.save()
        self.assertFalse(sch.is_player_available(mtg, player))

    def test_is_couple_available(self):
        """
        Must create a couple, then validate they work
        This is a trivial function however..
        """
        sch = Scheduler()
        mtg = self.meetings[0]
        guy = self.guys[0]
        girl = self.girls[0]
        av1 = PlayerAvailability.objects.get_for_season_player(
            season=self.season, player=guy)
        av2 = PlayerAvailability.objects.get_for_season_player(
            season=self.season, player=girl)
        couple = Couple(male=guy, female=girl)
        self.assertTrue(sch.is_couple_available(mtg, couple))

        av1.available[0] = False
        av1.save()

        self.assertFalse(sch.is_couple_available(mtg, couple))
        self.assertFalse(sch.is_couple_available(mtg, couple))
        self.assertFalse(sch.is_couple_available(mtg, couple))


class TestPlayStats(BlockDBTestBase):

    @classmethod
    def setUpTestData(cls):
        results = cls.staticCoreSetup()
        [cls.guys, cls.girls, cls.season, cls.meetings] = results
        cls.splayers = cls.staticPlayersSetup(
            cls.season,
            cls.girls,
            cls.guys)
        cls.couples = cls.static_couples_setup(
            cls.season,
            cls.girls,
            cls.guys)

    def setUp(self):
        pass

    @staticmethod
    def add_to_schedule(player, meetings, plays):
        for i, did_play in enumerate(plays):
            if did_play:
                try:
                    Schedule.objects.create(
                        meeting=meetings[i],
                        player=player
                    )
                except IntegrityError:
                    pass

    def add_couple_plays(self, couple, he, she):
        self.add_to_schedule(couple.male, self.meetings, he)
        self.add_to_schedule(couple.female, self.meetings, she)

    def test_play_stats_calc_no_plays(self):
        scheduler = Scheduler()
        couple = self.couples[1]

        info = scheduler.calc_play_stats_for_couple(self.season, couple)
        self.assertEqual(info.get('total_plays'), 0)
        self.assertEqual(info.get('weight'), 0)

    def test_play_stats_calc_with_plays(self):
        scheduler = Scheduler()
        couple = self.couples[1]
        self.add_couple_plays(couple,
                              [1, 1, 1, 1],
                              [1, 1, 1, 1])

        info = scheduler.calc_play_stats_for_couple(self.season, couple)
        self.assertEqual(info.get('total_plays'), 4)
        self.assertEqual(info.get('couple'), couple)
        # self.assertEqual(info.get('weight'), 0)

    def test_play_stats_calc_with_plays_1(self):
        scheduler = Scheduler()
        couple = self.couples[1]
        self.add_couple_plays(couple,
                              [1, 0, 1, 1],
                              [0, 1, 0, 1])

        info = scheduler.calc_play_stats_for_couple(self.season, couple)
        self.assertEqual(info.get('total_plays'), 4)
        self.assertEqual(info.get('weight'), 2.5)

    def test_play_stats_calc_with_plays_2(self):
        scheduler = Scheduler()
        couple = self.couples[1]
        self.add_couple_plays(couple,
                              [1, 0, 0, 1, 0, 1],
                              [0, 1, 0, 1, 0, 1])

        info = scheduler.calc_play_stats_for_couple(self.season, couple)
        self.assertEqual(info.get('total_plays'), 4)
        self.assertEqual(info.get('weight'), 3)

    def test_play_stats_calc_with_plays_3(self):
        scheduler = Scheduler()
        couple = self.couples[1]
        self.add_couple_plays(couple,
                              [1, 0, 0, 1, 0, 1],
                              [0, 0, 0, 1, 0, 1])

        info = scheduler.calc_play_stats_for_couple(self.season, couple)
        self.assertEqual(info.get('total_plays'), 3)
        self.assertEqual(info.get('weight'), 2.5)


class TestGroups(BlockDBTestBase):

    @classmethod
    def setUpTestData(cls):
        results = cls.staticCoreSetup()
        [cls.guys, cls.girls, cls.season, cls.meetings] = results
        cls.splayers = cls.staticPlayersSetup(
            cls.season,
            cls.girls,
            cls.guys)
        cls.couples = cls.static_couples_setup(
            cls.season,
            cls.girls,
            cls.guys,
            fulltime=[1, 0, 0, 0, 0, 0, 0, 0],
            singles=[0, 0, 0, 0, 0, 1, 1, 1])

        cls.season.courts=2
        cls.season.save()

    def setUp(self):
        pass

    def couples_modify(self, fulltime=None, singles=None):
        for i, couple in enumerate(self.couples):
            couple.fulltime = fulltime[i]
            couple.as_singles = singles[i]
            couple.save()

    @staticmethod
    def add_to_schedule(player, meetings, plays):
        for i, did_play in enumerate(plays):
            if did_play:
                try:
                    Schedule.objects.create(
                        meeting=meetings[i],
                        player=player
                    )
                except IntegrityError:
                    pass

    def test_get_next_group_meeting_one(self):
        """
        Test the initial version where there is no play history
        """
        scheduler = Scheduler()

        group = scheduler.get_next_group(with_singles=False)
        self.assertIsNotNone(group)
        self.assertEqual(len(group), 4)

    def test_get_next_group_with_history(self):
        """
        Test where there is some play history to consider
        Players or couples with no history should be added first.
        """
        pass
