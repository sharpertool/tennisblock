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

from .apiutils import JSONResponse, _currentSeason, SeasonSerializer

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
        cs = _currentSeason()
        if cs:
            serializer = SeasonSerializer(cs, many=False)
            return JSONResponse(serializer.data)
        else:
            return "Failed"

def getCurrentSeasonDates(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        cs = _currentSeason()
        if cs:
            startDate = cs.startdate
            endDate = cs.enddate

            return 'Nice'

    return 'Failure'

def getLatestBuzz(request):

    return JSONResponse([
        {'text': "Block starts September 20th"},
        {'text': "I don't know the holdout dates yet."}
    ])


