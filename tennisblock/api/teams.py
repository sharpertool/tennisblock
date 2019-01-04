from rest_framework.views import APIView
from rest_framework.response import Response

from TBLib.manager import TeamManager

from .apiutils import JSONResponse


class Teams(APIView):

    def get(self, request, date=None):
        print("pick_teams GET for date %s" % date)

        mgr = TeamManager()
        match_data = mgr.query_match(date)

        return Response({
            'status': 'GET Done',
            'date': date,
            'teams': match_data
        })

    def post(self, request, date=None):
        # Date can be part of the URL, or the post data.
        date = request.data.get('date', date)
        iterations = request.data.get('iterations', 10)
        tries = request.data.get('tries', 5)

        mgr = TeamManager()
        result = mgr.pick_teams_for_date(date,
                                         iterations=iterations,
                                         max_tries=tries)

        return Response(result)
