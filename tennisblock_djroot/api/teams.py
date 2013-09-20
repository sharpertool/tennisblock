# Create your views here.

import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from blockdb.models import Season,Couple,Player,SeasonPlayers,Meetings,Availability

from TennisBlock.schedule import Scheduler
from TennisBlock.teams import TeamManager

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

def pickTeams(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        mgr = TeamManager()

        teams = mgr.pickTeams(test=True,courts=3,sequences=3)

        return JSONResponse(teams)

