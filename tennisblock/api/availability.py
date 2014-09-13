# Create your views here.

import datetime
from django.views.generic.base import View
from rest_framework.parsers import JSONParser
from blockdb.models import Player,SeasonPlayers,Meetings,Availability,Schedule

from .apiutils import JSONResponse, get_current_season, get_meeting_for_date


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

        currseason = get_current_season()
        mtgs = Meetings.objects.filter(season = currseason).order_by('date')
        players = SeasonPlayers.objects.filter(season = currseason)

        pdata = []
        for sp in players:
            if not sp.blockmember:
                continue

            print("Getting availability data for %s" % sp.player.Name())

            player = sp.player

            avail = []
            scheduled = []

            nplayed = 0
            nscheduled = 0

            p = {
                'name' : player.user.first_name + ' ' + player.user.last_name,
                'id' : player.id,
                'isavail' : avail,
                'scheduled' : scheduled,
                'nplayed' : nplayed,
                'nscheduled': nscheduled
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
                    nscheduled += 1
                    if mtg.date < datetime.date.today():
                        nplayed += 1
                else:
                    scheduled.append(False)

            p['nplayed'] = nplayed
            p['nscheduled'] = nscheduled

            pdata.append(p)

        return JSONResponse(pdata)

    def put(self,request):
    #elif request.method == 'PUT':

        data = JSONParser().parse(request)
        currseason = get_current_season()
        mtgs = Meetings.objects.filter(season = currseason).order_by('date')
        try:
            mtg = mtgs[data['mtgidx']]
            p = Player.objects.get(pk=data['id'])
            print("Updating availability for %s on %s to %s" % (p.Name(),mtg.date,data['isavail']))
            av = Availability.objects.get(meeting=mtg,player=p)
            av.available = data['isavail']
            av.save()
        except:
            print("Error trying to update availability")

        #data = request.DATA
        # Update availability for someone.

        return JSONResponse({})

