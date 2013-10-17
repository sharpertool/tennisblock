# Create your views here.

import datetime
from django.views.generic.base import View
from rest_framework.parsers import JSONParser
from blockdb.models import Player,SeasonPlayers,Meetings,Availability,Schedule

from apiutils import JSONResponse, _currentSeason, _getMeetingForDate


def _AvailabilityInit(player,meetings):
    """
    Add blank availability items for the specified player
    """

    for mtg in meetings:
        av = Availability.objects.filter(meeting=mtg,player=player)

        if len(av)== 0:
            av = Availability.objects.create(
                meeting=mtg,
                player=player,
                available = True
            )
            av.save()


class AvailabilityView(View):

    def get(self,request):

        currseason = _currentSeason()
        mtgs = Meetings.objects.filter(season = currseason)
        players = SeasonPlayers.objects.filter(season = currseason)

        pdata = []
        for sp in players:
            if not sp.blockmember:
                continue

            player = sp.player

            avail = []
            scheduled = []

            p = {
                'name' : player.first + ' ' + player.last,
                'id' : player.id,
                'isavail' : avail,
                'scheduled' : scheduled
            }

            for mtg in mtgs:
                av = Availability.objects.filter(player=player, meeting=mtg)
                sch = Schedule.objects.filter(meeting=mtg,player=player)

                if len(av) == 0:
                    _AvailabilityInit(player,mtgs)
                    av = Availability.objects.filter(player=player, meeting=mtg)

                if len(av) > 0 and av[0].available:
                    avail.append(True)
                else:
                    avail.append(False)

                if len(sch):
                    scheduled.append(True)
                else:
                    scheduled.append(False)

            pdata.append(p)

        return JSONResponse(pdata)

    def put(self,request):
    #elif request.method == 'PUT':

        data = JSONParser().parse(request)
        currseason = _currentSeason()
        mtgs = Meetings.objects.filter(season = currseason)
        try:
            mtg = mtgs[data['mtgidx']]
            p = Player.objects.get(pk=data['id'])
            av = Availability.objects.get(meeting=mtg,player=p)
            av.available = data['isavail']
            av.save()
        except:
            print("Error trying to update availability")

        #data = request.DATA
        # Update availability for someone.

        return JSONResponse({})

