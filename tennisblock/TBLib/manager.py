# !/usr/bin/env python

from .teamgen.TeamGen import TeamGen
from .DBTeams import DBTeams
from api.apiutils import get_current_season


class TeamManager(object):
    def __init__(self, matchid=None):

        self.dbTeams = DBTeams()
        self.matchid = matchid

    def get_players(self, date=None):
        """ Retrive players for given date """
        men, women = self.dbTeams.get_players(date)

        assert ((len(men)+len(women)) % 4 == 0)
        return men, women

    def pick_teams_for_date(self,
                            date,
                            iterations: int = 100,
                            max_tries: int = 20):

        dbt = self.dbTeams
        dbt.delete_matchup(date)
        men, women = dbt.get_players(date)

        mgr = TeamManager()
        result = mgr.pick_teams(men=men, women=women,
                                iterations=iterations,
                                max_tries=max_tries)

        if result['status'] == 'success':
            result['match'] = mgr.query_match(date)

        return result

    def pick_teams(self, men=None, women=None, date=None, testing=False,
                   b_allow_duplicates=False, n_courts=None, n_sequences=3,
                   iterations: int = 100,
                   max_tries: int = 20):

        if men is None or women is None:
            men, women = self.get_players(date)

        # Calculate number fo courts from sum
        if n_courts is None:
            n_courts = (len(men)+len(women)) // 4

        #if len(men) < n_courts * 2 or len(women) < n_courts * 2:
        #    errmsg = """
        #    Cannot pick teams, there are not enough men or women.
        #    Need {0} of both. Have {1} men and {2} women.
        #    """.format(n_courts * 2, len(men), len(women))
        #    return {"status": "fail", "error": errmsg}

        tg = TeamGen(n_courts, n_sequences, men, women)
        sequences = tg.generate_set_sequences(
            b_allow_duplicates,
            iterations=iterations,
            max_tries=max_tries
        )

        if sequences is None or len(sequences) < n_sequences:
            return {"status": "fail",
                    "error": "Could not generate the required sequences"}

        else:
            # Put the worst sequences last.
            sequences.reverse()
            tg.display_sequences(sequences)
            tg.show_all_diffs(sequences)

            if not testing:
                self.dbTeams.insert_records(date, sequences)

            return {"status": "success"}

    def query_match(self, date=None):

        data = self.dbTeams.query_match(date)
        return data
