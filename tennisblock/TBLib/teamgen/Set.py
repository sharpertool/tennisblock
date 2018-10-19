class Set(object):
    def __init__(self):
        self.matches = []

    def clone(self):
        s = Set()
        s.matches = [m for m in self.matches]
        return s

    def add_match(self, match):
        self.matches.append(match)

    def set_diff(self):
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
            diffs.append(m.match_diff())

        diffs.sort()

        return diffs

    def diff_stats(self):
        diffMax = 0
        diffAvg = 0
        diffCnt = 0
        diffs = []

        for match in self.matches:
            diff = match.match_diff()

            diffCnt = diffCnt + 1
            diffAvg = diffAvg + diff
            if diff > diffMax:
                diffMax = diff
            diffs.append(diff)

        diffAvg = diffAvg / diffCnt
        diffs.sort()
        return diffMax, diffAvg, diffs

    def display(self):
        for match in self.matches:
            match.display()
            print("")

    def show_diffs(self):
        diffs = ["%4.2f" % match.match_diff() for match in self.matches]
        print("Diffs: " + "\t".join(diffs))

    def __str__(self):
        return " ".join([str(m) for m in self.matches])

    def __repr__(self):
        return str(self)
