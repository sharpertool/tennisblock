from rest_framework.request import Request
from .apiutils import get_current_season

from TBLib.teams import TeamManager

from .apiutils import JSONResponse

def pickTeams(request,date = None):
    """
    """
    r = Request(request)

    if r.method == 'POST':
        print("pickTeams POST for date %s" % date)
        matchData = {}
        season = get_current_season()
        if date and season:
            mgr = TeamManager()
            mgr.pickTeams(date,test=False,
                          courts=3,
                          sequences=3)

            matchData = mgr.queryMatch(date)

        return JSONResponse({'status' : 'POST Done','date' : date,'teams':matchData})

def queryTeams(request,date = None):
    """
    """
    r = Request(request)

    if r.method == 'GET':
        print("pickTeams GET for date %s" % date)
        matchData = {}
        if date:
            mgr = TeamManager()

            matchData = mgr.queryMatch(date)

        return JSONResponse({'status' : 'GET Done','date' : date,'teams':matchData})


