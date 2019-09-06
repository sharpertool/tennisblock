from blockdb.models import Season, SeasonPlayer, Couple

from rest_framework.views import APIView
from rest_framework.response import Response
from ..apiutils import JSONResponse, get_current_season as gcs, SeasonSerializer


def get_seasons(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        seasons = Season.objects.all()
        serializer = SeasonSerializer(seasons, many=True)
        return JSONResponse(serializer.data)


def get_current_season(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        cs = gcs()
        if cs:
            serializer = SeasonSerializer(cs, many=False)
            return JSONResponse(serializer.data)
        else:
            return "Failed"


def get_latest_buzz(request):
    return JSONResponse([
        {'text': "Block starts September 20th"},
        {'text': "I don't know the holdout dates yet."}
    ])


class CouplesView(APIView):

    def get(self, request, format=None):
        currseason = gcs()

        context = {}
        players = SeasonPlayer.objects.filter(season=currseason)
        couples = Couple.objects.filter(season=currseason)

        player_data = {'guys': [], 'girls': []}
        guys = player_data['guys']
        girls = player_data['girls']

        for sp in players:
            p = sp.player
            data = {
                'id': p.id,
                'spid': sp.id,
                'first': p.user.first_name,
                'last': p.user.last_name,
                'gender': p.gender
            }
            if p.gender == 'F':
                girls.append(data)
            else:
                guys.append(data)

        couple_data = []
        for c in couples:
            data = {
                'id': c.id,
                'girl': c.female.id,
                'guy': c.male.id,
                'fulltime': c.fulltime,
                'as_single': c.as_single,
            }
            couple_data.append(data)

        context['players'] = player_data
        context['couples'] = couple_data
        context['initial'] = {
            'season': currseason.id,
            'fulltime': False,
            'blockcouple': True,
            'canschedule': True
        }

        return Response(context)
