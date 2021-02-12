# !/usr/bin/env python

from django.conf import settings
from os.path import join
from teamgen.TeamGen import TeamGen
from teamgen.player import Player as TGPlayer
from .DBTeams import DBTeams
from teamgen.Team import Team
from teamgen.Match import Match
import jsonpickle
from datetime import datetime


class TeamManager(object):
    def __init__(self, matchid=None):

        self.dbTeams = DBTeams()
        self.matchid = matchid

    def get_players(self, date=None):
        """ Retrieve players for given date """
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
                            fteams: float = 1.0,
                            low_threshold: float = 0.75):

        Team.team_factor = fpartners
        Match.match_spread_factor = fteams

        dbt = self.dbTeams
        dbt.delete_matchup(date)
        men, women = self.get_players(date)

        result = self.pick_teams(men=men, women=women,
                                 date=date,
                                 iterations=iterations,
                                 max_tries=max_tries,
                                 low_threshold=low_threshold)

        if result['status'] == 'success':
            result['match'] = self.query_match(date)

        return result

    def pick_teams(self, men=None, women=None,
                   date=None, testing=False,
                   b_allow_duplicates=False,
                   n_courts=None, n_sequences=3,
                   iterations: int = 100,
                   max_tries: int = 20,
                   low_threshold: float = 0.75):

        if men is None or women is None:
            men, women = self.get_players(date)

        if n_courts is None:
            n_courts = (len(men) + len(women)) // 4

        now = datetime.now()
        player_file = f'players_{now.strftime("%Y-%m-%d_%H%M")}.json'
        with open(join(settings.MEDIA_ROOT, player_file)) as fp:
            data = {
                'men': men,
                'women': women,
                'n_courts': n_courts,
                'n_sequences': n_sequences,
                'iterations': iterations,
                'max_tries': max_tries,
                'low_threshold': low_threshold,
                'date': date,
                'b_allow_duplicates': b_allow_duplicates
            }
            frozen = jsonpickle.encode(data, indent=4)
            fp.write(frozen)

        # Calculate number fo courts from sum
        if n_courts is None:
            n_courts = (len(men) + len(women)) // 4

        tg = TeamGen(n_courts, n_sequences,
                     men, women,
                     low_threshold=low_threshold)
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
            # sequences.reverse()
            tg.display_sequences(sequences)
            tg.show_all_diffs(sequences)

            if not testing:
                self.dbTeams.insert_records(date, sequences)

            return {"status": "success"}

    def pick_match(self,
                   date,
                   setnumber=None,
                   iterations: int = 100,
                   max_tries: int = 20,
                   testing: bool = False,
                   fpartners: float = 1.0,
                   fteams: float = 1.0,
                   low_threshold: float = 0.75):

        Team.team_factor = fpartners
        Match.match_spread_factor = fteams

        dbt = self.dbTeams
        dbt.delete_match(date, setnumber)
        men, women = self.get_players(date)

        result = self.pick_new_match(men=men, women=women,
                                 iterations=iterations,
                                 max_tries=max_tries,
                                 low_threshold=low_threshold)

        if result['status'] == 'success':
            result['match'] = self.query_match(date)

        return result

    def pick_new_match(self, men=None, women=None,
                       date=None, setnumber=None,
                       testing=False,
                       b_allow_duplicates=False,
                       n_courts=None, n_sequences=3,
                       iterations: int = 100,
                       max_tries: int = 20,
                       low_threshold: float = 0.75):

        if men is None or women is None:
            men, women = self.get_players(date)

        # Calculate number fo courts from sum
        if n_courts is None:
            n_courts = (len(men) + len(women)) // 4

        tg = TeamGen(n_courts, n_sequences,
                     men, women,
                     low_threshold=low_threshold)

        # ToDo: Read existing data into history

        round = tg.generate_round(
            max_tries=max_tries
        )

        if round:
            # ToDo: Insert new round into DB
            return {"status": "success"}

        else:
            # Put the worst sequences first
            # sequences.reverse()
            # tg.display_sequences(sequences)
            # tg.show_all_diffs(sequences)

            # if not testing:
            #     self.dbTeams.insert_records(date, sequences)

            return {"status": "failed"}

    def query_match(self, date=None):

        data = self.dbTeams.query_match(date)
        return data
