class Match(object):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def match_diff(self):
        c1 = self.t1.microntrp()
        c2 = self.t2.microntrp()
        return abs(c1 - c2)

    def display(self):
        self.t1.display()
        print("Versus")
        self.t2.display()
        print("diff: %4.2f\n" % self.match_diff())

    def __str__(self):
        return f"{self.match_diff():3.2}"

    def __repr__(self):
        return str(self)
