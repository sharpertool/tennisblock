# !/usr/bin/env python

from .teamgen.TeamGen2 import TeamGen
from .teamgen.DBTeams import DBTeams


class TeamManager(object):
    def __init__(self, matchid=None):

        self.dbTeams = DBTeams()
        self.matchid = matchid

    def getPlayers(self, date=None):
        """ Retrive players for given date """
        men, women = self.dbTeams.getPlayers(date)

        assert (len(men) == len(women))
        return men, women

    def pickTeams(self, men=None, women=None, date=None, testing=False,
                  noDupes=False, nCourts=None, n_sequences=3):

        if men is None or women is None:
            men, women = self.getPlayers(date)

        # Calculate number fo courts based on # of men.
        # Assume # of women is the same.
        if nCourts is None:
            nCourts = len(men) // 2

        if len(men) < nCourts * 2 or len(women) < nCourts * 2:
            errmsg = "Cannot pick teams, there are not enough men or women."
            errmsg += "Need %d of both. Have %d men and %d women." % (nCourts * 2, len(men), len(women))
            return {"status": {"error": errmsg}}

        tg = TeamGen(nCourts, n_sequences, men, women)
        sequences = tg.generate_set_sequences(noDupes)

        if sequences is None or len(sequences) < n_sequences:
            return {"status": {"error": "Could not generate the required sequences"}}

        else:
            # Put the worst sequences last.
            sequences.reverse()
            tg.display_sequences(sequences)
            tg.show_all_diffs(sequences)

            if not testing:
                self.dbTeams.InsertRecords(date, sequences)

            return sequences

    def queryMatch(self, date=None):

        data = self.dbTeams.queryMatch(date)
        return data
