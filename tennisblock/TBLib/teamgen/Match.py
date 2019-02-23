from .Team import Team


class Match:
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

    def quality(self, fpartner: float = 3.0, fspread: float = 1.0):
        """
        Calcualte a quality score
        Lower numbers are better
        :return:
        """

        s1 = self.t1.spread()
        s2 = self.t2.spread()
        q1 = self.t1.inverse_quality(factor=fpartner)
        q2 = self.t2.inverse_quality(factor=fpartner)
        #d1 = self.t1.combined_microntrp()
        #d2 = self.t2.combined_microntrp()
        self._quality = round(10 - (q1+q2) - fspread * (s1+s2), 1)
        return self._quality

    def display(self):
        self.t1.display()
        print("Versus")
        self.t2.display()
        print(f"diff:{self._diff:4.2} "
              f"Quality:{self._quality:4.2}\n")

    def __str__(self):
        return f"{self._diff:3.2}"

    def __repr__(self):
        return str(self)
