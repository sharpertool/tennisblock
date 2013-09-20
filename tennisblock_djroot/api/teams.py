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

from apiutils import JSONResponse

def pickTeams(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        mgr = TeamManager()

        teams = mgr.pickTeams(test=True,courts=3,sequences=3)

        return JSONResponse(teams)

