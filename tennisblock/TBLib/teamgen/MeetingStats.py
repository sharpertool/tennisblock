import random
from typing import List
from TBLib.teamgen.exceptions import NoValidOpponent, NoValidPartner

from .Match import Match
from .Team import Team
from .Set import Set


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
        self.setList: List[Set] = []

        self.maxIterations = 100
        self.minDiff = 10
        self.nFailuresByInvalidPartner = 0
        self.nFailuresByDiff = 0

        self.seeGirlsOnlyOnce = False
        if self.n_courts == 3:
            self.seeGirlsOnlyOnce = False

        self.chkMatchups = 0
        self.chkH2H = 0
        self.chkPairs = 0

        self.Opponents = {}
        self.Partners = {}
        self.Opposites = {}
        self.Opposites2X = {}
        self.InvalidFemOpponents = {}
        self.InvalidFemPartners = {}

        self.specialCase = self.is_special_case()

        self.minDiffHistory = []

        # Need a reverse lookup table
        self.pbyname = {}
        for p in self.men + self.women:
            self.pbyname[p.Name()] = p

    def set_see_partner_once(self, b_once):
        if b_once:
            print("Setting the see Girls setting to True")
            self.maxIterations *= 10
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
            self.Opposites[p.Name()] = set()
            self.Opponents[p.Name()] = set()
            self.Opposites2X[p.Name()] = set()
        for p in self.men:
            self.InvalidFemOpponents[p.Name()] = set()
            self.InvalidFemPartners[p.Name()] = set()

        print("restart Done")

    def is_special_case(self):
        """
        Grrr - this is special for Sheryl, who asks to play with Kirby!
        Hah!!! Mike isn't on our block, and neither is Sheryl/
        """
        # for m in self.men:
        #     if m.Name() == 'Dickhead':
        #         for w in self.women:
        #             if w.Name() == 'Vagina':
        #                 return True
        return False

    def diff_history_min(self):
        return min(self.minDiffHistory)

    def add_set(self, new_set):
        """
        Once we have a valid set, then add it to the list and update
        all of the variables we use to track the statisics for this run.

        """
        for match in new_set.matches:
            m1 = match.t1.p1.Name()
            f1 = match.t1.p2.Name()
            m2 = match.t2.p1.Name()
            f2 = match.t2.p2.Name()

            # Do both directions
            self.Opponents[m1].add(m2)
            self.Opponents[m2].add(m1)
            self.Opponents[f1].add(f2)
            self.Opponents[f2].add(f1)

            # Do partners m->f
            self.Partners[m1].add(f1)
            self.Partners[m2].add(f2)

            # Do opposites
            if f2 in self.Opposites[m1]:
                self.Opposites2X[m1].add(f2)
            else:
                self.Opposites[m1].add(f2)

            if f1 in self.Opposites[m2]:
                self.Opposites2X[m2].add(f1)
            else:
                self.Opposites[m2].add(f1)

        for m in self.men:
            mn = m.Name()
            if self.seeGirlsOnlyOnce:
                m_invalid = self.Partners[mn].union(self.Opposites[mn])
            else:
                m_invalid = self.Partners[mn].intersection(
                    self.Opposites[mn])
                m_invalid = m_invalid.union(self.Opposites2X[mn])
            self.InvalidFemOpponents[mn] = m_invalid

            if self.seeGirlsOnlyOnce:
                p_invalid = self.Partners[mn].union(self.Opposites[mn])
            else:
                p_invalid = self.Partners[mn].union(self.Opposites2X[mn])
            self.InvalidFemPartners[mn] = p_invalid

        print("Added a set")

    def clear_check_stats(self):
        self.nFailuresByInvalidPartner = 0
        self.nFailuresByDiff = 0
        self.minDiff = 10

    def print_check_stats(self):
        print(f"Failed Stats:Partner:{self.nFailuresByInvalidPartner}"
              f"Diff:{self.nFailuresByDiff} Mindiff:{self.minDiff}")

    def get_new_set(self, diff_max):
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
        max_tries = 20
        new_set: Set = None

        while new_set is None and tries < max_tries:
            print(f"Trying to build a set DiffMax:{diff_max:5.3} Try # {tries}.")
            new_set = self.build_set(diff_max)
            tries += 1

        return new_set

    def build_set(self, diff_max) -> Set:
        """
        First, build a set of matches with men only.
        Next, add in the women. The men are assigned
        randomly, so it should not matter what the women
        are assigned as later.. they will be assigned
        randomly to the men.
        """
        n_tries = 0
        max_tries = self.maxIterations

        self.minDiffHistory = [diff_max]

        self.setList = []

        while n_tries < max_tries / 10:
            t_men, t_women = self.get_temp_list()

            # Build sets of men first.
            # If there is an exception thrown, then just ignore
            # it and try again..
            while True:
                try:
                    new_set = self.init_set(t_men)
                    break
                except NoValidOpponent:
                    print("Regenerate the set of men")
                    pass
            self.display_update(n_tries, diff_max)
            self.clear_check_stats()
            # Initialize High, then set to lowest value found
            self.minDiff = 10
            try:
                if self.add_women(new_set, t_women, diff_max, self.maxIterations):
                    return new_set
                self.print_check_stats()
                self.minDiffHistory.append(self.minDiff)
            except NoValidPartner:
                # we can continue on here.
                pass
            n_tries = n_tries + 1

        return None

    def add_women(self, aset, t_women, diff_max, max_tries):
        """
        Upon entry, aset will be a set that contains
        the male pairings, but with no women entered. The
        male pairings will have been done randomly, so
        they should be okay.
        """

        n_tries = 0
        n_continue = True
        while n_continue and n_tries < max_tries:
            s_women = set(t_women)
            random.seed()
            try:
                for m in aset.matches:
                    m.t1.p2 = None
                    m.t2.p2 = None

                    m1 = m.t1.p1.Name()
                    m2 = m.t2.p1.Name()

                    f1 = self.valid_partner(m1, m2, s_women, None)
                    s_women.remove(f1)

                    f2 = self.valid_partner(m2, m1, s_women, f1)
                    s_women.remove(f2)

                    m.t1.p2 = self.pbyname[f1]
                    m.t2.p2 = self.pbyname[f2]

                curr_diff = max(aset.diff())
                if curr_diff <= diff_max:
                    return True

                # Ah.. keep track of minimum diff found for a set
                # Later, I'll track these minimum diffs, and then use that
                # as the next diff_max!
                self.minDiff = min(self.minDiff, curr_diff)
                self.nFailuresByDiff = self.nFailuresByDiff + 1
                self.setList.append(aset.clone())

            except NoValidPartner as e:
                raise

            # We have a bad one..
            n_tries = n_tries + 1

        # If we make it here.. we failed
        return False

    def valid_partner(self, m1, m2, s_women, f1=None):
        """
        Pick a woman that is a valid partner for the two men specified in m1 and m2.

        The rule is -
        If a woman has played with AND against m2, she is not a valid opponent
        M2 will have seen her 3 times.
        Also if she has played against M2 2x already, she can't play against him again.

        f1 is set to the first female in the current group if this is the second call.
        """

        # m2_invalid = self.Partners[m2].intersection(self.Opposites[m2])
        # m2_invalid = m2_invalid.union(self.Opposites2X[m2])
        m2_invalid = self.InvalidFemOpponents[m2]

        # s_invalid = self.Partners[m1].union(self.Opposites2X[m1])
        m1_invalid = self.InvalidFemPartners[m1]
        s_invalid = m1_invalid.union(m2_invalid)

        if f1:
            s_invalid = s_invalid.union(self.Opponents[f1])

        tmp = s_women.difference(s_invalid)
        if len(tmp) == 0:
            raise NoValidPartner()

        partner = random.choice(list(tmp))
        return partner

    def valid_opponent(self, player, opponents):
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

    def get_temp_list(self):

        t_men = [x.Name() for x in self.men]
        t_women = [x.Name() for x in self.women]
        return t_men, t_women

    def init_set(self, t_men):
        """
        Build a new set with a list of men that are valid opponents of each other.

        Each time this function is called, a new random set of men should be chosen.
        The only history used is the history of men that have played against each other
        this night. The valid_opponent function is used for this determination.
        """
        new_set = Set()
        s_men = set(t_men)

        for n in range(0, self.n_courts):
            m1 = random.choice(list(s_men))
            s_men.remove(m1)
            m2 = self.valid_opponent(m1, s_men)
            s_men.remove(m2)
            m = Match(Team(self.pbyname[m1], None),
                      Team(self.pbyname[m2], None))
            new_set.add_match(m)
        return new_set

