# Create your views here.

import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from blockdb.models import Season,Couple,Player,SeasonPlayers,Meetings,Availability
from rest_framework.request import Request

from TBLib.schedule import Scheduler
from TBLib.teams import TeamManager

from apiutils import JSONResponse

def pickTeams(request,date = None):
    """
    """
    r = Request(request)

    if r.method == 'GET':
        print("pickTeams GET for date %s" % date)
        mgr = TeamManager()

        #teams = mgr.pickTeams(test=True,courts=3,sequences=3)

        return JSONResponse({'status' : 'GET Done','date' : date})
    elif r.method == 'POST':
        print("pickTeams POST for date %s" % date)
        if date:
            mgr = TeamManager()
            teams = mgr.pickTeams(test=False,courts=3,sequences=3)

        return JSONResponse({'status' : 'POST Done','date' : date,'teams':teams})


