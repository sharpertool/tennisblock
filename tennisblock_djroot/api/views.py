# Create your views here.

import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from blockdb.models import Season,Couple,Player

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = (
            'id',
            'name',
            'courts',
            'firstcourt',
            'startdate',
            'enddate'
        )

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def getSeasons(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        seasons = Season.objects.all()
        serializer = SeasonSerializer(seasons, many=True)
        return JSONResponse(serializer.data)

def getCurrentSeason(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        seasons = Season.objects.filter(enddate__gte = datetime.date.today())
        if len(seasons) > 0:
            serializer = SeasonSerializer(seasons[0], many=False)
            return JSONResponse(serializer.data)
        else:
            return "Failed"

def getCurrentSeasonDates(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        seasons = Season.objects.filter(enddate__gte = datetime.date.today())
        if len(seasons) > 0:
            season = seasons[0]
            startDate = season.startdate
            endDate = season.enddate

            return 'Nice'

    return 'Failure'

def getLatestBuzz(request):

    return JSONResponse([
        {'text': "Block starts September 20th"},
        {'text': "I don't know the holdout dates yet."}
    ])


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
