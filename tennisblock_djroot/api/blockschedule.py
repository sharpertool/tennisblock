# Create your views here.

import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import serializers
from blockdb.models import Season,Couple,Player,SeasonPlayers,Meetings,Availability

from apiutils import JSONResponse, _currentSeason

def _BuildMeetings(force=False):
    """
    Build the meetings for the current season if they don't exist..

    """

    currSeason = _currentSeason()
    if not currSeason:
        return

    if force:
        # Remove existing meetings if we are forcing this.
        # Note that this will also remove all 'Availability' for these meetings.
        Meetings.objects.filter(season=currSeason).delete()

    meetings = Meetings.objects.filter(season=currSeason)

    if len(meetings) > 0:
        # Looks like we are good
        return

    startDate = currSeason.startdate
    endDate = currSeason.enddate
    blockStart = currSeason.blockstart
    blocktime = currSeason.blocktime

    dates = []
    currDate = blockStart
    while currDate <= endDate:
        mtg = Meetings.objects.create(
            season=currSeason,
            date=currDate,
            holdout=False,
            comments="")
        mtg.save()
        currDate += datetime.timedelta(days = 7)

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


def getBlockPlayers(request):

    if request.method == 'GET':
        couples = Couple.objects.all()
        data = []
        for c in couples:
            d = {
                'name' : c.name,
                'him' : c.male.first + ' ' + c.male.last,
                'her' : c.female.first + ' ' + c.female.last
            }
            data.append(d)

        return JSONResponse(data)


def BlockDates(request):

    if request.method == 'GET':
        currSeason = _currentSeason()

        meetings = Meetings.objects.filter(season=currSeason)
        mtgData = []
        for mtg in meetings:
            mtgData.append({
                'date' : mtg.date,
                'holdout' : mtg.holdout
            })

        response = JSONResponse(mtgData)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


    return JSONResponse({'status' : "Failed"})


def PlayerAvailability(request):

    if request.method == "GET":
        currseason = _currentSeason()
        mtgs = Meetings.objects.filter(season = currseason)
        players = SeasonPlayers.objects.filter(season = currseason)

        pdata = []
        for sp in players:
            if not sp.blockmember:
                continue

            player = sp.player

            p = {
                'name' : player.first + ' ' + player.last,
                'id' : player.id,
                'isavail' : []
            }
            avail = p['isavail']
            for mtg in mtgs:
                av = Availability.objects.filter(player=player, meeting=mtg)

                if len(av) == 0:
                    _AvailabilityInit(player,mtgs)
                    av = Availability.objects.filter(player=player, meeting=mtg)

                if len(av) > 0 and av[0].available:
                    avail.append(True)
                else:
                    avail.append(False)

            pdata.append(p)

        return JSONResponse(pdata)

    elif request.method == 'PUT':

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
