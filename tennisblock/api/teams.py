from rest_framework.request import Request

from TBLib.manager import TeamManager

from .apiutils import JSONResponse


def pick_teams(request, date=None):
    """
    """
    r = Request(request)

    if r.method == 'POST':
        print("pick_teams POST for date %s" % date)
        mgr = TeamManager()
        match_data = mgr.pick_teams_for_date(date)

        return JSONResponse({'status': 'POST Done',
                             'date': date, 'teams': match_data})


def query_teams(request, date=None):
    """
    """
    r = Request(request)

    if r.method == 'GET':
        print("pick_teams GET for date %s" % date)
        match_data = {}
        if date:
            mgr = TeamManager()
            match_data = mgr.query_match(date)

        return JSONResponse({'status': 'GET Done',
                             'date': date, 'teams': match_data})
