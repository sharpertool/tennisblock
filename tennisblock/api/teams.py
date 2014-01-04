# Create your views here.

import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from tennisblock.blockdb.models import Season,Couple,Player,SeasonPlayers,Meetings,Availability
from rest_framework.request import Request

from tennisblock.TBLib.schedule import Scheduler
from tennisblock.TBLib.teams import TeamManager

from .apiutils import JSONResponse

def pickTeams(request,date = None):
    """
    """
    r = Request(request)

    if r.method == 'POST':
        print("pickTeams POST for date %s" % date)
        matchData = {}
        if date:
            mgr = TeamManager()
            mgr.pickTeams(date,test=False,courts=3,sequences=3)

            matchData = mgr.queryMatch(date)

        return JSONResponse({'status' : 'POST Done','date' : date,'teams':matchData})

def queryTeams(request,date = None):
    """
    """
    r = Request(request)

    if r.method == 'GET':
        print("pickTeams GET for date %s" % date)
        matchData = {}
        if date:
            mgr = TeamManager()

            matchData = mgr.queryMatch(date)

        return JSONResponse({'status' : 'GET Done','date' : date,'teams':matchData})


