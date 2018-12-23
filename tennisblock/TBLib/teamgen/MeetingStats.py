import random
from typing import List
from collections import Counter, defaultdict
from TBLib.teamgen.exceptions import NoValidOpponent, NoValidPartner

from .Match import Match
from .Team import Team
from .round import MatchRound


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

        self.maxIterations = 100
        self.n_fails_by_invalid_partner = 0
        self.n_fails_by_diff = 0

        self.seeGirlsOnlyOnce = False
        if self.n_courts == 3:
            self.seeGirlsOnlyOnce = False

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
            self.pbyname[p.Name()] = p

        self.log_level = 0

        # Should do this only once
        random.seed()

    def set_see_partner_once(self, b_once):
        if b_once:
            print("Setting the see Girls setting to True")
            # self.maxIterations *= 10
        else:
            print("Setting the see Girls setting to False")
        self.seeGirlsOnlyOnce = b_once

    def set_max_iteration(self, n):
        self.maxIterations = n

    def restart(self):
        """
        Clear all statistics and restart the checking
        """

        self.Partners = {}
        self.Opponents = {}
        self.Opposites = {}
        for p in self.men + self.women:
            self.Partners[p.Name()] = set()
            self.Opposites[p.Name()] = Counter()
            self.Opponents[p.Name()] = set()
        for p in self.men:
            self.InvalidOpponents[p.Name()] = set()
            self.InvalidPartners[p.Name()] = set()

        print("restart Done")

    def diff_history_min(self):
        return min(self.diff_history)

    def add_round(self, new_round):
        """
        Once we have a valid set, then add it to the list and update
        all of the variables we use to track the statisics for this run.

        """
        max_cnt = 1 if self.seeGirlsOnlyOnce else 2

        for match in new_round.matches:
            m1 = match.t1.p1.Name()
            f1 = match.t1.p2.Name()
            m2 = match.t2.p1.Name()
            f2 = match.t2.p2.Name()
            match_players = [m1, f1, m2, f2]

            # Do both directions
            self.Opponents[m1].add(m2)
            self.Opponents[m2].add(m1)
            self.Opponents[f1].add(f2)
            self.Opponents[f2].add(f1)

            # Do partners m->f
            self.Partners[m1].add(f1)
            self.Partners[m2].add(f2)
            self.Partners[f1].add(m1)
            self.Partners[f2].add(m2)

            # Increment the count of times played with opposites
            self.Opposites[m1].update({f2})
            self.Opposites[m2].update({f1})
            self.Opposites[f2].update({m1})
            self.Opposites[f1].update({m2})

            # Increment the Seen count for all players
            for i in match_players:
                self.Seen[i].update({j for j in match_players if j is not i})

        self.update_invalids()

    def update_invalids(self):
        """
        Iterate of the  men and update the invalid partner or opposite sex
        opponent for each
        :return:
        """
        for m in self.men:
            self.update_invalids_for_player(m, see_once=self.seeGirlsOnlyOnce)

    def update_invalids_for_player(self, player, see_once=True):
        """
        Taking a men->women approach, we determine a list of invalid women opponents
        and invalid women partners. 
        If we set see_once to True, then we can only play with or against the same woman
        once. If false, we can play with and against, but not with 2x or against 2x.
        
        
        :param player: 
        :param see_once: 
        :return: 
        """
        if player.gender == 'M':
            gender_set = self.women
        else:
            gender_set = self.men

        gender_names = [i.Name() for i in gender_set]

        name = player.Name()
        op = self.Opposites[name]
        opset = set(op)
        seen = self.Seen[name]

        if see_once:
            # Invalid partner OR opponent if we have seen them already
            invalid = set({i for i in gender_names if seen[i] >= 1})
            self.InvalidOpponents[name] = invalid
            self.InvalidPartners[name] = invalid

        else:
            # Allowed to see them 2 times, but once as partner, once as opposite
            invalid = set({i for i in gender_names if seen[i] >= 2})
            self.InvalidOpponents[name] = invalid.union(self.Partners[name])
            self.InvalidPartners[name] = invalid.union(opset)

    def get_new_round(self, diff_max, quality_max, max_tries=20):
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
        new_round: MatchRound = None

        min_diff = 1000.0
        min_q = 1000.0
        max_build_tries = self.maxIterations

        while new_round is None and tries < max_tries:
            self.diff_history = []
            self.quality_history = []
            new_round = self.build_round(max_build_tries, diff_max, quality_max)
            tries += 1
            md = 0.0
            mq = 0.0
            if self.diff_history and self.quality_history:
                md = min(self.diff_history)
                mq = min(self.quality_history)
                min_diff = min(min_diff, md)
                min_q = min(min_q, mq)
            print(f"Build a set DiffMax:{diff_max:5.3}({md:5.3}) MinQ:{quality_max:5.3}({mq:5.3}) Try:{tries}.")

        return new_round, min_diff, min_q

    def build_round(self, max_tries, diff_max, quality_max) -> MatchRound:
        """
        First, build a set of matches with men only.
        Next, add in the women. The men are assigned
        randomly, so it should not matter what the women
        are assigned as later.. they will be assigned
        randomly to the men.
        """
        n_tries = 0

        while n_tries < max_tries:
            t_men, t_women = self.get_temp_list()

            # Build sets of men first.
            # If there is an exception thrown, then just ignore
            # it and try again..
            new_round = self.pick_men(t_men)

            self.clear_check_stats()

            try:
                if self.add_women(new_round, t_women,
                                  diff_max, quality_max,
                                  max_tries):
                    return new_round
                self.print_check_stats()
            except NoValidPartner:
                # we can continue on here, regenerate the men matchups
                pass
            n_tries = n_tries + 1

        return None

    def add_women(self, new_round: MatchRound, t_women: set,
                  diff_max: int, quality_max: int, num_tries: int) -> bool:
        """
        Upon entry, new_round will be a set that contains
        the male pairings, but with no women entered. The
        male pairings will have been done randomly, so
        they should be okay.
        """
        curr_diff = diff_max + 1
        curr_q = quality_max + 1
        min_diff = 1000
        min_q = 1000

        while num_tries and (curr_diff > diff_max or curr_q > quality_max):
            s_women = set(t_women)

            for m in new_round.matches:
                m1 = m.t1.p1.Name()
                m2 = m.t2.p1.Name()

                f1 = self.get_valid_partner(m1, m2, s_women, None)
                s_women.remove(f1)

                f2 = self.get_valid_partner(m2, m1, s_women, f1)
                s_women.remove(f2)

                m.t1.p2 = self.pbyname[f1]
                m.t2.p2 = self.pbyname[f2]

            curr_diff = max(new_round.diff())
            curr_q = max(new_round.quality())

            min_diff = min(min_diff, curr_diff)
            min_q = min(min_q, curr_q)

            num_tries -= 1
            #if curr_diff > diff_max or curr_q > quality_max:
            #    print(f"[add_women] {num_tries} {round(curr_diff-diff_max, 1)} {round(curr_q-quality_max, 1)}")

        self.diff_history.append(min_diff)
        self.quality_history.append(min_q)

        return curr_diff <= diff_max and curr_q <= quality_max

    def get_valid_partner(self, m1, m2, s_women, f1=None):
        """
        Pick a woman that is a valid partner for the two men specified in m1 and m2.

        The rule is -
        If a woman has played with AND against m2, she is not a valid opponent
        M2 will have seen her 3 times.
        Also if she has played against M2 2x already, she can't play against him again.

        f1 is set to the first female in the current group if this is the second call.
        """

        invalid = self.InvalidOpponents[m2].union(self.InvalidPartners[m1])

        if f1:
            invalid = invalid.union(self.Opponents[f1])

        tmp = s_women.difference(invalid)
        if len(tmp) == 0:
            raise NoValidPartner()

        partner = random.choice(list(tmp))
        return partner

    def get_temp_list(self):

        t_men = [x.Name() for x in self.men]
        t_women = [x.Name() for x in self.women]
        return t_men, t_women

    def pick_men(self, t_men):
        """
        Build a new set with a list of men that are valid opponents of each other.

        Each time this function is called, a new random set of men should be chosen.
        The only history used is the history of men that have played against each other
        this night. The get_valid_opponent function is used for this determination.
        """
        random.seed()

        while True:
            new_round = MatchRound()
            s_men = set(t_men)
            try:
                for n in range(0, self.n_courts):
                    m1 = random.choice(list(s_men))
                    s_men.remove(m1)
                    m2 = self.get_valid_opponent(m1, s_men)
                    s_men.remove(m2)
                    m = Match(Team(self.pbyname[m1]),
                              Team(self.pbyname[m2]))
                    new_round.add_match(m)
                return new_round
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
        if self.log_level > 0:
            print(f"Failed Stats:Partner:{self.n_fails_by_invalid_partner}"
                  f"Diff:{self.n_fails_by_diff} Mindiff:{min(self.diff_history)}")
