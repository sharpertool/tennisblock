import logging
from .player import Player

logger = logging.getLogger(__name__)


class Team:
    """
    Represents a pair of players on a team.

    max_diff is the maximum variation we would expect,
    so a 2.0 with a 5.0
    """
    quality_factor = 1.0
    max_diff = 3.0

    def __init__(self, player1=None, player2=None):
        self.p1: Player = player1
        self.p2: Player = player2

    def combined_microntrp(self):
        """
        Expecting a mixed team.
        If there are 2 ladies, i.e. we were short a guy, then make a slight
        reduction in combined to compensate

        If this is 2 men, then make a slight increase.

        """
        if self.p1.gender == 'F' and self.p1.gender == 'F':
            combined = 0.92 * self.p1.microntrp + self.p2.microntrp
        elif self.p1.gender == 'M' and self.p1.gender == 'M':
            combined = 1.08 * (self.p1.microntrp + self.p2.microntrp)
        else:
            combined = self.p1.microntrp + self.p2.microntrp
        return combined

    def spread(self):
        return abs(self.p1.microntrp - self.p2.microntrp)

    def quality(self, factor=None):
        """ Range from 100 as best, to zero as worst we calculate """
        factor = factor or self.quality_factor
        diff = min(self.max_diff, factor * abs(self.p1.microntrp - self.p2.microntrp))
        Q = round(100 - 100 * (diff / self.max_diff))
        return Q

    def display(self):
        p1 = self.p1
        p2 = self.p2
        logger.info(
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
                f" @ {un1 + un2:3.2} {un1}/{un2}")

    def __repr__(self):
        str(self)
