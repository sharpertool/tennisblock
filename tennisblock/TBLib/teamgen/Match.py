from .Team import Team


class Match:
    def __init__(self, t1: Team, t2: Team):
        self.t1 = t1
        self.t2 = t2

    def match_diff(self):
        c1 = self.t1.combined_microntrp()
        c2 = self.t2.combined_microntrp()
        return abs(c1 - c2)

    def match_quality(self):
        """
        Calcualte a quality score
        Lower numbers are better
        :return:
        """
        s1 = self.t1.spread()
        s2 = self.t2.spread()
        d1 = self.t1.combined_microntrp()
        d2 = self.t2.combined_microntrp()
        quality = abs(d1-d2)+s1+s2
        return quality

    def display(self):
        self.t1.display()
        print("Versus")
        self.t2.display()
        print("diff: %4.2f\n" % self.match_diff())

    def __str__(self):
        return f"{self.match_diff():3.2}"

    def __repr__(self):
        return str(self)
