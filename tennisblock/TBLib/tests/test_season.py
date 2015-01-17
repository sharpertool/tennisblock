__author__ = 'kutenai'
from django.test import TestCase

from TBLib.season import SeasonManager

class TestSeason(TestCase):


    def test_get_current_season(self):

        sm = SeasonManager()
        meetings = sm.get_meeting_list()

