from .Team import Team


class Match:
    def __init__(self, t1: Team, t2: Team):
        self.t1 = t1
        self.t2 = t2

    def diff(self):
        c1 = self.t1.combined_microntrp()
        c2 = self.t2.combined_microntrp()
        return round(abs(c1 - c2), 1)

    def quality(self):
        """
        Calcualte a quality score
        Lower numbers are better
        :return:
        """
        s1 = self.t1.spread()
        s2 = self.t2.spread()
        d1 = self.t1.combined_microntrp()
        d2 = self.t2.combined_microntrp()
        quality = round(abs(d1 - d2) + s1 + s2, 1)
        return quality

    def display(self):
        self.t1.display()
        print("Versus")
        self.t2.display()
        print(f"diff:{self.diff():4.2} "
              f"Quality:{self.quality():4.2}\n")

    def __str__(self):
        return f"{self.diff():3.2}"

    def __repr__(self):
        return str(self)
