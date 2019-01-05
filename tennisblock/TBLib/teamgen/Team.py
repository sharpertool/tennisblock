from blockdb.models import Player


class Team:
    """
    Represents a pair of players on a team.
    """

    def __init__(self, player1=None, player2=None):
        self.p1: Player = player1
        self.p2: Player = player2

    def combined_microntrp(self):
        """
        P1 will be a guy, or if this is 2 ladies, a gal and then p2
        will be a gal.  In this case, p1 gets downgraded as they are
        playing "as a guy", theoretically.

        """
        if self.p1.gender == 'F':
            combined = 0.92*self.p1.microntrp + self.p2.microntrp
        else:
            combined = self.p1.microntrp + self.p2.microntrp
        return combined

    def spread(self):
        return abs(self.p1.microntrp - self.p2.microntrp)

    def display(self):
        p1 = self.p1
        p2 = self.p2
        print(
            f"{p1 and p1.name} {p1 and p1.ntrp:3.2}/"
            f"{p1 and p1.microntrp:3.2}"
            f" and "
            f"{p2 and p2.name} {p2 and p2.ntrp:3.2}/"
            f"{p2 and p2.microntrp:3.2}"
            f" = {p1 and p2 and self.combined_microntrp():3.2}")

    def __str__(self):
        name1 = ''
        name2 = '---'
        un1 = 0.0
        un2 = 0.0
        if self.p1:
            name1 = self.p1.name
            un1 = self.p1.microntrp

        if self.p2:
            name2 = self.p2.name
            un2 = self.p2.microntrp

        return (f"{name1} and {name2}"
                f" @ {un1+un2:3.2}")

    def __repr__(self):
        str(self)
