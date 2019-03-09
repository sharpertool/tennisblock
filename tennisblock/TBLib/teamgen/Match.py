from .Team import Team


class Match:
    """
    Worst diff is a pair of 2.0's against a pair of 5.0's
        abs(10.0 - 4.0) or 6.0
    """
    diff_max = 6.0

    def __init__(self, t1: Team, t2: Team):
        self.t1 = t1
        self.t2 = t2
        self._quality = None
        self._diff = None

    def diff(self):
        c1 = self.t1.combined_microntrp()
        c2 = self.t2.combined_microntrp()
        self._diff = round(abs(c1 - c2), 1)
        return self._diff

    def diff_quality(self, fspread: float = 1.0):
        """ Quality of team play from 0 to 100 """
        diff = self.diff()
        return 100 - 100 * (diff / self.diff_max)

    def quality(self, fpartner: float = 1.0, fspread: float = 1.0):
        """
        Calculate a quality score
        100 is ideal, 0 is lowest

        q1 and q1 both range from 0 to 100
        diff
        :return:
        """
        # Calculate weights
        total = fpartner + fpartner + fspread
        pct_partner = fpartner / total
        pct_spread = fspread / total
        pct_partner_half = pct_partner / 2

        Qd = self.diff_quality()
        Q1 = self.t1.quality(factor=fpartner)
        Q2 = self.t2.quality(factor=fpartner)
        Q = (pct_partner * Q1
             + pct_partner * Q2
             + pct_spread * Qd)
        self._quality = Q
        return round(self._quality)

    def display(self):
        self.t1.display()
        print("Versus")
        self.t2.display()
        print(f"diff:{self._diff:4.2} "
              f"Quality:{self._quality:4.2}\n")

    def __str__(self):
        return f"{self.t1} vs {self.t2} {self._diff:3.2} {self._quality:3.1}"

    def __repr__(self):
        return str(self)
