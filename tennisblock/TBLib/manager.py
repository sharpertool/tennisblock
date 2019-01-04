# !/usr/bin/env python

from .teamgen.TeamGen import TeamGen
from .teamgen.DBTeams import DBTeams


class TeamManager(object):
    def __init__(self, matchid=None):

        self.dbTeams = DBTeams()
        self.matchid = matchid

    def get_players(self, date=None):
        """ Retrive players for given date """
        men, women = self.dbTeams.get_players(date)

        #assert (len(men) == len(women))
        return men, women

    def pick_teams(self, men=None, women=None, date=None, testing=False,
                   b_allow_duplicates=False, n_courts=None, n_sequences=3,
                   iterations=None):

        if men is None or women is None:
            men, women = self.get_players(date)

        # Calculate number fo courts based on # of men.
        # Assume # of women is the same.
        if n_courts is None:
            n_courts = (len(men)+len(women)) // 4
            print(f"Determined default number of courts as {n_courts}")

        # if len(men) < n_courts * 2 or len(women) < n_courts * 2:
        #     errmsg = "Cannot pick teams, there are not enough men or women."
        #     errmsg += "Need %d of both. Have %d men and %d women." % (n_courts * 2, len(men), len(women))
        #     return {"status": {"error": errmsg}}

        tg = TeamGen(n_courts, n_sequences, men, women)
        sequences = tg.generate_set_sequences(b_allow_duplicates, iterations=iterations)

        if sequences is None or len(sequences) < n_sequences:
            return {"status": {"error": "Could not generate the required sequences"}}

        else:
            # Put the worst sequences last.
            sequences.reverse()
            tg.display_sequences(sequences)
            tg.show_all_diffs(sequences)

            if not testing:
                self.dbTeams.insert_records(date, sequences)

            return sequences

    def query_match(self, date=None):

        data = self.dbTeams.query_match(date)
        return data
