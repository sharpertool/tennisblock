from unittest import TestCase
from collections import namedtuple

from TBLib.teamgen import Match, Player, Team, MatchRound


class TeamTests(TestCase):

    @staticmethod
    def buildMatch(ntrp=None):
        t1 = Team(
            player1=Player(0, 'M', ntrp[0], ntrp[0], '', 'M1'),
            player2=Player(0, 'F', ntrp[1], ntrp[1], '', 'F1'),
        )
        t2 = Team(
            player1=Player(0, 'M', ntrp[2], ntrp[2], '', 'M1'),
            player2=Player(0, 'F', ntrp[3], ntrp[3], '', 'F1'),
        )
        return Match(t1, t2)

    @staticmethod
    def buildRound(ntrp_set=None, fspread=1.0, fpartner=1.0):
        r = MatchRound()
        for ntrp in ntrp_set:
            r.add_match(TeamTests.buildMatch(ntrp))

        return r

    def test_basic_round(self):
        r = self.buildRound([
            [3.5, 4.0, 4.0, 3.5],
            [2.5, 4.5, 3.0, 3.5],
            [4.0, 4.0, 3.5, 4.5]])

        q = r.quality_average
        qexp = 82
        self.assertEqual(q, qexp, f"Expected Q of {qexp} for {r}")

    def test_great_round(self):
        r = self.buildRound([
            [3.5, 4.0, 4.0, 3.5],
            [3.5, 4.5, 4.0, 3.5],
            [4.0, 4.0, 3.5, 4.5]])

        q = r.quality_average
        qexp = 86
        self.assertEqual(qexp, q, f"Expected Q of {qexp} for {r}")

    def test_perfect_round(self):
        r = self.buildRound([
            [4.0, 4.0, 4.0, 4.0],
            [4.0, 4.0, 4.0, 4.0],
            [4.0, 4.0, 4.0, 4.0]])

        q = r.quality_average
        qexp = 100
        self.assertEqual(qexp, q, f"Expected Q of {qexp} for {r}")
