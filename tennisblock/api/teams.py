from rest_framework.views import APIView
from rest_framework.response import Response

from TBLib.manager import TeamManager

from .apiutils import JSONResponse


class Teams(APIView):

    def get(self, request, date=None):
        print("pick_teams GET for date %s" % date)

        match_data = {}

        mgr = TeamManager()
        match_data = mgr.query_match(date)

        return Response({
            'status': 'GET Done',
            'date': date,
            'teams': match_data
        })

    def post(self, request, date=None):
        print("pick_teams POST for date %s" % date)

        iterations = request.POST.get('iterations', 10)
        max_tries = request.POST.get('max_tries', 5)

        mgr = TeamManager()
        match_data = mgr.pick_teams_for_date(date,
                                             iterations=iterations,
                                             max_tries=max_tries)

        return Response({
            'status': 'POST Done',
            'date': date,
            'teams': match_data
        })
