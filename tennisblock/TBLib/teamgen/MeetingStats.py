import logging
import random
from typing import List
from collections import Counter, defaultdict
from TBLib.teamgen.exceptions import NoValidOpponent, NoValidPartner

from .Match import Match
from .Team import Team
from .round import MatchRound

logger = logging.getLogger(__name__)


def make_key(m, f):
    return "%s %s:%s %s" % (m.first, m.last, f.first, f.last)


def make_sorted_key(a, b):
    if a.pid < b.pid:
        return make_key(a, b)
    else:
        return make_key(b, a)


class MeetingStats:
    def __init__(self, n_courts, n_sets, men, women):
        self.n_courts = n_courts
        self.n_sets = n_sets
        self.men = men
        self.women = women
        self.all = men + women

        self.round_template = None

        self._max_iterations = 100
        self.n_fails_by_invalid_partner = 0
        self.n_fails_by_diff = 0

        self._see_player_once = False
        if self.n_courts == 3:
            self._see_player_once = False

        self.chkMatchups = 0
        self.chkH2H = 0
        self.chkPairs = 0

        self.Opponents = {}
        self.Partners = {}
        self.Seen = defaultdict(Counter)
        self.Opposites = {}
        self.InvalidOpponents = {}
        self.InvalidPartners = {}

        self.diff_history = []
        self.quality_history = []

        # Need a reverse lookup table
        self.pbyname = {}
        for p in self.men + self.women:
            self.pbyname[p.name] = p

        self.log_level = 0

        # Should do this only once
        random.seed()

    @property
    def see_player_once(self):
        return self._see_player_once

    @see_player_once.setter
    def see_player_once(self, value):
        if value:
            logger.debug("Setting the see_player_once setting to True")
        else:
            logger.debug("Setting the see_player_once setting to False")
        self._see_player_once = value

    @property
    def max_iterations(self):
        return self._max_iterations

    @max_iterations.setter
    def max_iterations(self, n):
        self._max_iterations = n

    def restart(self):
        """
        Clear all statistics and restart the checking
        """

        self.Partners = {}
        self.Opponents = {}
        self.Opposites = {}
        for p in self.men + self.women:
            self.Partners[p.name] = set()
            self.Opposites[p.name] = Counter()
            self.Opponents[p.name] = set()
            self.InvalidOpponents[p.name] = set()
            self.InvalidPartners[p.name] = set()

        logger.debug("restart Done")

    def diff_history_min(self):
        return min(self.diff_history)

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
            t1 = [t1p1, t1p2]
            t2 = [t2p1, t2p2]
            match_players = [t1p1, t1p2, t2p1, t2p2]

            # Add all opponents to set
            [self.Opponents[x].update(t2) for x in t1]
            [self.Opponents[x].update(t1) for x in t2]

            # Add all partners to set
            for t in [t1, t2]:
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
        for m in self.men:
            self.update_invalids_for_player(
                m,
                see_once=self.see_player_once)

    def update_invalids_for_player(self, player, see_once=True):
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

        if see_once:
            # Invalid partner OR opponent if we have seen them already
            invalid = set([i for i in names if seen[i] >= 1])
            self.InvalidOpponents[name] = invalid
            self.InvalidPartners[name] = invalid

        else:
            # Allowed to see them 2 times, but once as partner, once as opposite
            invalid = set([i for i in names if seen[i] >= 2])
            self.InvalidOpponents[name] = invalid.union(self.Partners[name])
            self.InvalidPartners[name] = invalid.union(set(self.Opposites[name]))

    def get_new_round(self, diff_max=1.0, quality_min=90, max_tries=20):
        """
        This one needs to use the existing sets and list and pick a new
        randomization of the available sets.
        """

        """
        - Pick a guy
            - Pick an opponent from list of available opponents - men 
            not played yet
            - Pick two women from list of available women 
            (checking opposites, pairs)
        - From remaining guys, repeat the above.. and then for the last 
        set
        """
        tries = 0
        self.round_template = MatchRound()
        rounds: MatchRound = None

        min_diff = 1000.0
        minq = maxq = 0
        min_min_q = 100
        max_max_q = 0
        max_build_tries = self.max_iterations

        while rounds is None and tries < max_tries:
            self.diff_history = []
            self.quality_history = []
            rounds = self.build_round(max_build_tries, diff_max, quality_min)
            tries += 1
            md = 0.0
            if self.diff_history and self.quality_history:
                md = min(self.diff_history)
                maxq = max(self.quality_history)
                minq = min(self.quality_history)
                min_diff = min(min_diff, md)
                min_min_q = min(min_min_q, minq)
                max_max_q = max(max_max_q, maxq)

            logger.debug(
                f"Build a set DiffMax:{diff_max:5.3}({md:5.3})"
                f" MinQ:{quality_min:5.1f}({minq:5.1f}, {maxq:5.1f}) Try:{tries}.")

        return rounds, min_diff, min_min_q, max_max_q

    def build_round(self, iterations, diff_max, quality_min) -> MatchRound:
        """
        First, build a set of matches with men only.
        Next, add in the women. The men are assigned
        randomly, so it should not matter what the women
        are assigned as later.. they will be assigned
        randomly to the men.
        """

        diff = len(self.men) - len(self.women)
        if diff % 2:
            raise Exception("We have an odd number of players!")

        if diff % 4 != 0:
            return self.build_balanced_round(iterations, diff_max, quality_min)

        if diff > 0:
            g1 = self.men
            g2 = self.women
        else:
            g1 = self.women
            g2 = self.men

        return self.build_unbalanced_round(iterations,
                                           diff_max,
                                           quality_min,
                                           g1, g2)

    def build_unbalanced_round(self,
                               iterations,
                               diff_max,
                               quality_min,
                               g1, g2):

        assert(len(g1) > len(g2))
        diff = len(g1) - len(g2)

        n_tries = 0

        while n_tries < iterations:
            t1 = [x.name for x in g1]
            t2 = [x.name for x in g2]

            if abs(diff) == 4:
                """ Hard code this for now... """
                set1 = set(t1)
                set2 = set(t2)
                set1a = set(random.sample(set1, k=4))
                set1b = set1.copy()
                set1b -= set1a
                assert(len(set2) == len(set1b))

                round1, set1a_partners = self.pick_first_group(set1a, courts=1)
                round2, set1b_partners = self.pick_first_group(set1b, courts=3)

                self.clear_check_stats()

                try:
                    if all([
                        self.add_partners(round1, set1a_partners,
                                          diff_max, quality_min,
                                          iterations),
                        self.add_partners(round2, set2,
                                          diff_max, quality_min,
                                          iterations),
                    ]):
                        return [round1, round2]
                    self.print_check_stats()

                except NoValidPartner:
                    # we can continue on here, regenerate the men matchups
                    pass
            n_tries = n_tries + 1

        return None

    def build_balanced_round(self, iterations,
                             diff_max, quality_min,
                             ):
        """ Build a round with equal numbers of men and women """

        n_tries = 0

        while n_tries < iterations:
            t_men, t_women = self.get_temp_list()

            # Build sets of men first.
            # If there is an exception thrown, then just ignore
            # it and try again..
            round = self.pick_first_group(t_men)

            self.clear_check_stats()

            try:
                if self.add_partners(round, t_women,
                                  diff_max, quality_min,
                                  iterations):
                    return round
                self.print_check_stats()
            except NoValidPartner:
                # we can continue on here, regenerate the men matchups
                pass
            n_tries = n_tries + 1

        return None

    def add_partners(self, round: MatchRound, p_list: list,
                  diff_max: int, quality_min: int, num_tries: int) -> bool:
        """
        Upon entry, round will be a set that contains
        the initial partner, but with no 2nd partner entered. The
        initial pairints pairings will have been done randomly, so
        they should be okay.
        """
        curr_diff = diff_max + 1
        curr_q = 100
        min_diff = 1000
        max_q = 0

        while num_tries and (curr_diff > diff_max or curr_q < quality_min):
            p_set = set(p_list)

            for m in round.matches:
                m1 = m.t1.p1.name
                m2 = m.t2.p1.name

                f1 = self.get_valid_partner(m1, m2, p_set, None)
                p_set.remove(f1)

                f2 = self.get_valid_partner(m2, m1, p_set, f1)
                p_set.remove(f2)

                m.t1.p2 = self.pbyname[f1]
                m.t2.p2 = self.pbyname[f2]

            diffs = round.diff
            qualities = round.quality

            # We want the worst case values here.
            curr_diff = max(diffs)
            curr_q = min(qualities)

            min_diff = min(min_diff, curr_diff)

            num_tries -= 1

        self.diff_history.append(min_diff)
        # We want the best case value here
        self.quality_history.extend(qualities)

        return curr_diff <= diff_max and curr_q >= quality_min

    def get_valid_partner(self, m1, m2, p_set, f1=None):
        """
        Pick a partner that is a valid partner for the two players specified in m1 and m2.

        The rule is -
        If a player has played with AND against m2, they are not a valid opponent
        M2 will have seen them 3 times.
        Also if they have played against M2 2x already, they can't play against them again.

        f1 is set to the first player in the current group if this is the second call.
        """

        invalid = self.InvalidOpponents[m2].union(self.InvalidPartners[m1])

        if f1:
            invalid = invalid.union(self.Opponents[f1])

        tmp = p_set.difference(invalid)
        if len(tmp) == 0:
            raise NoValidPartner()

        partner = random.choice(list(tmp))
        return partner

    def get_temp_list(self, g1=None, g2=None):
        if g1 is None:
            g1 = self.men
        if g2 is None:
            g2 = self.women

        t_men = [x.name for x in g1]
        t_women = [x.name for x in g2]

        d = len(t_men) - len(t_women)
        if d != 0:

            if d % 4 == 0:
                # We can work with this.
                # return t_men, t_women
                pass

            if d > 0:
                big, sm = t_men, t_women
            else:
                big, sm = t_women, t_men

            while d:
                p = random.choice(list(big))
                sm.append(p)
                big.remove(p)
                d = len(t_men) - len(t_women)

        return t_men, t_women

    def pick_first_group(self, players, courts=None):
        """
        Build a new set with a list of players from the first group.
        The first group may be men or women, depends on which set is
        larger.

        Each time this function is called, a new random set of players should be chosen.
        The only history used is the history of players that have played against each other
        this night. The get_valid_opponent function is used for this determination.
        """
        random.seed()

        if courts is None:
            courts = self.n_courts

        while True:
            round = self.round_template.clone()
            pset = set(players)
            try:
                for n in range(0, courts):
                    m1 = random.choice(list(pset))
                    pset.remove(m1)
                    m2 = self.get_valid_opponent(m1, pset)
                    pset.remove(m2)
                    m = Match(Team(self.pbyname[m1]),
                              Team(self.pbyname[m2]))
                    round.add_match(m)
                return round, pset
            except NoValidOpponent:
                pass

    def get_valid_opponent(self, player, opponents):
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

    def clear_check_stats(self):
        self.n_fails_by_invalid_partner = 0
        self.n_fails_by_diff = 0

    def print_check_stats(self):
        logger.debug(f"Failed Stats:Partner:{self.n_fails_by_invalid_partner}"
                    f"Diff:{self.n_fails_by_diff} Mindiff:{self.diff_history and min(self.diff_history)}")
