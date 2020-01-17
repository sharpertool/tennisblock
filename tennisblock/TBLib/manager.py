# !/usr/bin/env python

from .teamgen.TeamGen import TeamGen
from .teamgen.player import Player as TGPlayer
from .DBTeams import DBTeams
from api.apiutils import get_current_season
from .teamgen.Team import Team
from .teamgen.Match import Match


class TeamManager(object):
    def __init__(self, matchid=None):

        self.dbTeams = DBTeams()
        self.matchid = matchid

    def get_players(self, date=None):
        """ Retrive players for given date """
        men, women = self.dbTeams.get_players(date)

        make_player = lambda p: TGPlayer(p.pk, p.gender, p.ntrp, p.microntrp, p.phone, p.name)

        assert ((len(men) + len(women)) % 4 == 0)
        tg_men = [make_player(p) for p in men]
        tg_women = [make_player(p) for p in women]
        return tg_men, tg_women

    def pick_teams_for_date(self,
                            date,
                            iterations: int = 100,
                            max_tries: int = 20,
                            testing: bool = False,
                            fpartners: float = 1.0,
                            fteams: float = 1.0):

        Team.team_factor = fpartners
        Match.match_spread_factor = fteams

        dbt = self.dbTeams
        dbt.delete_matchup(date)
        men, women = self.get_players(date)

        result = self.pick_teams(men=men, women=women,
                                 iterations=iterations,
                                 max_tries=max_tries)

        if result['status'] == 'success':
            result['match'] = self.query_match(date)

        return result

    def pick_teams(self, men=None, women=None,
                   date=None, testing=False,
                   b_allow_duplicates=False,
                   n_courts=None, n_sequences=3,
                   iterations: int = 100,
                   max_tries: int = 20):

        if men is None or women is None:
            men, women = self.get_players(date)

        # Calculate number fo courts from sum
        if n_courts is None:
            n_courts = (len(men) + len(women)) // 4

        tg = TeamGen(n_courts, n_sequences, men, women)
        sequences = tg.generate_rounds(
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
