from django.test import TestCase

from TBLib.DBTeams import DBTeams
from TBLib.teamgen import (Meeting, MatchRound, Team, Player)


class TestBalancedRound:

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_get_history(self):
        """

        """
        db = DBTeams()
        history = db.get_history()
        pass