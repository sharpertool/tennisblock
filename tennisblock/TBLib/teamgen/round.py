from typing import List
import math

from .Match import Match


class MatchRound:
    def __init__(self, fpartner: float = 3.0, fspread: float = 1.0):
        self.matches: List[Match] = []
        self.fpartner = fpartner
        self.fspread = fspread

    def clone(self):
        s = MatchRound(fpartner=self.fpartner, fspread=self.fspread)
        s.matches = [m for m in self.matches]
        return s

    def add_match(self, match: Match):
        self.matches.append(match)

    def diff(self):
        """
        Take all diff values, put them in a list.

        Return the sorted list.. later, I'll write a comparison
        algorithm.

        Return the max diff value, the worst match, and then
        the second max value, i.e. the 2nd worst match. This
        would allow me to prefer a set that has 3 great matches
        and one bad one, over a set that has potentially 4 bad matches..

        Consider two cases:
          0.5,0.6,0.5,0.6

          0.1,0.0,0.2,0.6

        In the previous algorithm, they are the same... here, the second
        one could be preferred.

        """
        diffs = []
        for m in self.matches:
            diffs.append(m.diff())

        diffs.sort()

        return diffs

    def quality(self):
        return [
            m.quality(fpartner=self.fpartner, fspread=self.fspread)
            for m in self.matches
        ]

    def diff_stats(self):
        diffs = [m.diff() for m in self.matches]
        # qvals = [m.quality() for m in self.matches]
        diffs.sort()
        return max(diffs), sum(diffs) / len(diffs), diffs

    def display(self):
        for match in self.matches:
            match.display()
            print("")

    def show_diffs(self):
        diffs = ["%4.2f" % match.diff() for match in self.matches]
        print("Diffs: " + "\t".join(diffs))

    def __str__(self):
        return " ".join([str(m) for m in self.matches])

    def __repr__(self):
        return str(self)
