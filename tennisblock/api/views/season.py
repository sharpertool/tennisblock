from blockdb.models import Season, SeasonPlayer, Couple, Player

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
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


class CouplesView(APIView):

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None, season_id=None):

        currseason = get_object_or_404(Season, pk=season_id) if season_id else gcs()

        context = {}
        players = SeasonPlayer.objects.filter(season=currseason).all()
        couples = Couple.objects.filter(season=currseason).all()

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
                'name': c.name,
                'guy': c.male.id,
                'girl': c.female.id,
                'fulltime': c.fulltime,
                'as_singles': c.as_singles,
                'blockcouple': c.blockcouple,
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

    def post(self, request):
        """
        Update the couples. Expected input:

            couples -- array
            couple: {
              name: 'Name for this couple, i.e. Hendersons',
              guy: <player id of the guy>,
              girl: <player id of the girl>,
              fulltime: <boolean if they are fulltime>,
              as_singles: <boolean if they are coupled as singles>,
          }

        """
        currseason = gcs()
        couples = request.data.get('couples', [])

        result = {
            'status': 'success',
            'updated': [],
            'created': [],
        }

        current_id_list =[]

        for index, couple in enumerate(couples):
            id = couple.get('id')
            name = couple.get('name', '')
            guy = couple.get('guy')
            girl = couple.get('girl')
            fulltime = couple.get('fulltime')
            as_singles = couple.get('as_singles')

            male = Player.objects.get(id=guy)
            female = Player.objects.get(id=girl)

            try:
                if id is not None:
                    c = Couple.objects.get(pk=id)
                else:
                    c = Couple.objects.get(season=currseason, male=male, female=female)
                c.as_singles = as_singles
                c.fulltime = fulltime
                c.name = name
                c.save()

                result['updated'].append({
                    'id': c.id,
                    'index': index,
                })
                current_id_list.append(c.id)

            except Couple.DoesNotExist:
                c = Couple(
                    season=currseason,
                    name=name,
                    male=male,
                    female=female,
                    fulltime=fulltime,
                    as_singles=as_singles,
                    canschedule=True,
                    blockcouple=True
                   )
                c.save()
                current_id_list.append(c.id)

                result['created'].append({
                    'id': c.id,
                    'index': index,
                    'name': c.name,
                })

        # Now, remove extra couples!
        Couple.objects.filter(~Q(id__in=current_id_list)).delete()

        return Response(result)

