from rest_framework.request import Request
from .apiutils import get_current_season

from TBLib.manager import TeamManager
from TBLib.teamgen.DBTeams import DBTeams

from .apiutils import JSONResponse


def pick_teams(request, date=None):
    """
    """
    r = Request(request)

    if r.method == 'POST':
        print("pick_teams POST for date %s" % date)
        matchData = {}
        season = get_current_season()
        if date and season:
            dbTeams = DBTeams()

            men, women = dbTeams.get_players(date)
            mgr = TeamManager()
            mgr.pick_teams(men=men, women=women, testing=False,
                           n_sequences=3, b_allow_duplicates=False)

            matchData = mgr.query_match(date)

        return JSONResponse({'status': 'POST Done', 'date': date, 'teams': matchData})


def query_teams(request, date=None):
    """
    """
    r = Request(request)

    if r.method == 'GET':
        print("pick_teams GET for date %s" % date)
        matchData = {}
        if date:
            mgr = TeamManager()

            matchData = mgr.query_match(date)

        return JSONResponse({'status': 'GET Done', 'date': date, 'teams': matchData})
