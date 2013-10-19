# Create your views here.


from django.views.generic.edit import View

from blockdb.models import Player,SeasonPlayers

from api.apiutils import JSONResponse,JSONParser, _currentSeason

class SeasonPlayersView(View):
    members_only = True

    def get(self,request):

        currseason = _currentSeason()
        players = SeasonPlayers.objects.filter(season = currseason).order_by('player__last','player__first')

        pdata = []
        for sp in players:

            player = sp.player

            p = {
                'id'            : player.id,
                'first'         : player.first,
                'last'          : player.last,
                'gender'        : player.gender,
                'ntrp'          : player.ntrp,
                'microntrp'     : player.microntrp,
                'email'         : player.email,
                'phone'         : player.phone,
                'blockmember'   : sp.blockmember
            }

            pdata.append(p)

        return JSONResponse(pdata)

    def put(self,request):

        data = JSONParser().parse(request)
        currseason = _currentSeason()

        return JSONResponse({})

