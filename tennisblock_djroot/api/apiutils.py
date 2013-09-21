# Create your views here.

import datetime
from django.http import HttpResponse
from dateutil import parser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import serializers
from blockdb.models import Season,Slot,Meetings

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


def _currentSeason():

    seasons = Season.objects.filter(enddate__gte = datetime.date.today())
    if len(seasons) > 0:
        return seasons[0]

    return None


def _nextMeeting(season):
    meetings = Meetings.objects \
        .order_by('date') \
        .filter(season=season, holdout=0,date__gte = datetime.date.today())

    mtg = None
    if len(meetings) > 0:
        mtg = meetings[0]

    return mtg

def _getMeetingForDate(date):

    season = _currentSeason()

    if not date:
        return _nextMeeting(season)

    dt = parser.parse(date)
    meetings = Meetings.objects \
        .order_by('date') \
        .filter(season=season) \
        .filter(date__exact = dt.strftime("%Y-%m-%d"))

    if len(meetings) == 1:
        return meetings[0]

    return None


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

def _getBlockSchedule(date=None):
    season = _currentSeason()
    mtg = _getMeetingForDate(date)

    slots = Slot.objects.order_by('set','court','position').filter(meeting=mtg)

    dbsets      = Slot.objects.filter(meeting=mtg).values('set').distinct()
    dbcourts    = Slot.objects.filter(meeting=mtg).values('court').distinct()
    dbpos       = Slot.objects.filter(meeting=mtg).values('position').distinct()

    sets = [s['set'] for s in dbsets]
    courts = [s['court'] for s in dbcourts]
    positions = [s['position'] for s in dbpos]


    sched = []

    currset = 0
    currcrt = 0

    schedule = {
        'sets' : sets,
        'courts' : courts,
        'positions' : positions,
        'sched' : {}
    }

    for slot in slots:
        # Initialize each set structure
        if currset != slot.set:
            currset = slot.set
            schedule['sched'][slot.set] = {}
            csArray = schedule['sched'][slot.set]
            for court in courts:
                csArray[court] = {
                    'ta' : {
                        'guy' : None,
                        'gal' : None
                    },
                    'tb' : {
                        'guy' : None,
                        'gal' : None
                    }
                }

        court = csArray[slot.court]
        pos = slot.position[0:2]
        pinfo = {
            'name' : slot.player.Name(),
            'ntrp' : slot.player.ntrp,
            'untrp': slot.player.microntrp
        }
        if slot.player.gender == 'F':
            court[pos]['gal'] = pinfo
        else:
            court[pos]['guy'] = pinfo


    return schedule
