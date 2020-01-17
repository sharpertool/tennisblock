import logging
import random
from typing import List
import itertools
from collections import Counter, defaultdict
from TBLib.teamgen.exceptions import NoValidOpponent, NoValidPartner

from .Match import Match
from .Team import Team
from .round import MatchRound
from .stats import RoundStats
from .player import Player
from .history import HistoryBase

logger = logging.getLogger(__name__)


def make_key(m, f):
    return "%s %s:%s %s" % (m.first, m.last, f.first, f.last)


def make_sorted_key(a, b):
    if a.pid < b.pid:
        return make_key(a, b)
    else:
        return make_key(b, a)


class MeetingHistory(HistoryBase):
    def __init__(self, group1, group2, see_player_once=False):

        super().__init__(see_player_once=see_player_once)

        self.group1 = group1
        self.group2 = group2

        self.Opponents = {}
        self.Partners = {}
        self.Seen = defaultdict(Counter)
        self.Opposites = {}
        self.InvalidOpponents = {}
        self.InvalidPartners = {}

        # Should do this only once
        random.seed()

    def restart(self):
        """
        Clear all statistics and restart the checking
        """

        self.Partners = {}
        self.Opponents = {}
        self.Opposites = {}
        for p in self.group1 + self.group2:
            self.Partners[p.name] = set()
            self.Opposites[p.name] = Counter()
            self.Opponents[p.name] = set()
            self.InvalidOpponents[p.name] = set()
            self.InvalidPartners[p.name] = set()

    def add_round(self, new_round):
        """
        Once we have a valid set, then add it to the list and update
        all of the variables we use to track the statisics for this run.

        """
        for match in new_round.matches:
            t1p1 = match.t1.p1.name
            t1p2 = match.t1.p2.name
            t2p1 = match.t2.p1.name
            t2p2 = match.t2.p2.name
            t1players = [t1p1, t1p2]
            t2players = [t2p1, t2p2]
            match_players = [t1p1, t1p2, t2p1, t2p2]

            # Add all opponents to set
            [self.Opponents[x].update(t2players) for x in t1players]
            [self.Opponents[x].update(t1players) for x in t2players]

            # Add all partners to set
            for t in [t1players, t2players]:
                self.Partners[t[0]].add(t[1])
                self.Partners[t[1]].add(t[0])

            # Increment the count of times played with any player
            for p in match_players:
                tmp = list(filter(lambda x: x is not p, match_players))
                self.Opposites[p].update(tmp)
                self.Seen[p].update(tmp)

        self.update_invalids()

    def update_invalids(self):
        """
        Iterate of the  men and update the invalid partner or opposite sex
        opponent for each
        :return:
        """
        for player in self.group1:
            self.update_invalids_for_player(player)

    def update_invalids_for_player(self, player):
        """
        If see_once is True, then we can only play with or against
        a particular player 1 time.
        If false, we could play with a player, and also against that
        same player, but not against the same player 2 times and
        not with the same player 2 times.

        :param player: 
        :param see_once: 
        :return: 
        """
        name = player.name
        seen = self.Seen[name]

        names = [i.name for i in self.all]

        if self.see_player_once:
            # Invalid partner OR opponent if we have seen them already
            invalid = set([i for i in names if seen[i] >= 1])
            self.InvalidOpponents[name] = invalid
            self.InvalidPartners[name] = invalid

        else:
            # Allowed to see them 2 times, but once as partner, once as opposite
            invalid = set([i for i in names if seen[i] >= 2])
            self.InvalidOpponents[name] = invalid.union(self.Partners[name])
            self.InvalidPartners[name] = invalid.union(set(self.Opposites[name]))

    def get_valid_partner(self, players: List[Player], available: List[Player]) -> Player:
        """
        Pick a partner that is a valid partner for the two players specified in m1 and m2.

        The rule is -
        If a player has played with AND against m2, they are not a valid opponent
        M2 will have seen them 3 times.
        Also if they have played against M2 2x already, they can't play against them again.

        f1 is set to the first player in the current group if this is the second call.
        """

        invalid = set()
        for player in players:
            invalid = invalid.union(self.InvalidOpponents[player])

        tmp = available.difference(invalid)
        if len(tmp) == 0:
            raise NoValidPartner()

        partner = random.choice(list(tmp))
        return partner

    def get_valid_opponent(self, player, opponents) -> Player:
        """
        The difference line retrieves a list of same-sex players that have
        not been opponents to this player yet.

        Implements the rule that men only play against other men
        once, and women only play against other women once.

        """

        tmp = opponents.difference(self.Opponents[player])
        if len(tmp) == 0:
            raise NoValidOpponent(player=player)

        opponent = random.choice(list(tmp))
        return opponent

