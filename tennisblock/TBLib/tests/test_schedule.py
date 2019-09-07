__author__ = 'kutenai'
from django.test import TestCase

from TBLib.season import SeasonManager
from TBLib.schedule import Schedule

from blockdb.tests.db_utils import BlockDBTestBase

class TestAvailability(BlockDBTestBase):

    def setUp(self):
        self.coreSetup()
        self.playersSetup()

    def test_is_player_available(self):

        sm = SeasonManager()
        meetings = sm.get_meeting_list()

