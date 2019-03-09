from rest_framework.views import APIView
from rest_framework.response import Response

from TBLib.manager import TeamManager

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
        fpartners = request.data.get('fpartners', 1.0)
        fteams = request.data.get('fteams', 1.0)

        mgr = TeamManager()
        result = mgr.pick_teams_for_date(date,
                                         iterations=iterations,
                                         max_tries=tries,
                                         fpartners=fpartners,
                                         fteams=fteams)

        return Response(result)
