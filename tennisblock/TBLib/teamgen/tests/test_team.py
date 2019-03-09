from unittest import TestCase
from collections import namedtuple

from TBLib.teamgen import Match, Player, Team


class TeamTests(TestCase):

    def setUp(self):
        self.players = []
        self.men = []
        self.women = []
        for i, ntrp in enumerate(range(4, 11)):
            ntrp = ntrp / 2
            for j, g in enumerate(['M', 'F']):
                p = Player(i * 10 + j, g, ntrp, ntrp, '', f'{g}{i}')
                self.players.append(p)
                self.men.append(p) if g == 'M' else self.women.append(p)

        self.team1 = Team(player1=self.men[6], player2=self.women[0])
        self.team2 = Team(player1=self.men[4], player2=self.women[3])
        self.team3 = Team(player1=self.men[4], player2=self.women[4])
        self.team4 = Team(player1=self.men[2], player2=self.women[5])

    def buildMatch(self, n1,  n2, n3, n4):
        t1 = Team(
            player1=Player(0, 'M', n1, n1, '', 'M1'),
            player2=Player(0, 'F', n2, n2, '', 'F1'),
        )
        t2 = Team(
            player1=Player(0, 'M', n3, n3, '', 'M1'),
            player2=Player(0, 'F', n4, n4, '', 'F1'),
        )
        return Match(t1, t2)

    def test_worst_spread(self):
        t = self.team1
        q = t.quality()
        qexp = 0
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for spread of {t.spread()}")

    def test_bad_spread(self):
        """ 100 - 100*(2.5/3.0)"""
        t = self.team4
        q = t.quality()
        qexp = 50
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for spread of {t.spread()}")

    def test_typical_spread(self):
        """ 100 - 100*(2.5/3.0)"""
        t = self.team2
        q = t.quality()
        qexp = 83
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for spread of {t.spread()}")

    def test_best_spread(self):
        t = self.team3
        q = t.quality()
        qexp = 100
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for spread of {t.spread()}")

    def test_team_quality_low(self):
        t = [self.team1, self.team2]
        m = Match(t[0], t[1])

        q = m.quality()
        qexp = 58
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for {m}")

    def test_team_quality_low_factor(self):
        t = [self.team1, self.team2]
        m = Match(t[0], t[1])

        q = m.quality(fspread=2.0)
        qexp = 67
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for {m}")

    def test_team_quality_low_factor2(self):
        t = [self.team1, self.team2]
        m = Match(t[0], t[1])

        q = m.quality(fspread=3.0)
        qexp = 72
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for {m}")

    def test_team_quality_low_factor3(self):
        t = [self.team1, self.team2]
        m = Match(t[0], t[1])

        q = m.quality(fpartner=0.5, fspread=1.0)
        qexp = 81
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for {m}")

    def test_team_quality_spread(self):
        t = [self.team2, self.team3]
        m = Match(t[0], t[1])

        q = m.quality()
        qexp = 92
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for {m}")

    def test_team_quality_perfect(self):
        t = [self.team3, self.team3]
        m = Match(t[0], t[1])

        q = m.quality()
        qexp = 100
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for {m}")

    def test_match_type(self):
        m = self.buildMatch(3.5, 4.0, 3.5, 4.5)

        q = m.quality()
        qexp = 81
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for {m}")

    def test_match_type_spread_priority(self):
        m = self.buildMatch(3.5, 4.0, 3.5, 4.0)

        q = m.quality(fspread=2.0)
        qexp = 92
        self.assertEquals(q, qexp, f"Expected Q of {qexp} for {m}")
