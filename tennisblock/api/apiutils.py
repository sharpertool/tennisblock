# Create your views here.

import datetime,time
from django.http import HttpResponse
from dateutil import parser
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
from blockdb.models import Season,Meetings

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


def get_current_season():
    """
    Return the current season object.
    """

    seasons = Season.objects.filter(enddate__gte = datetime.date.today())
    if len(seasons) > 0:
        return seasons[0]

    return None


def get_next_meeting(season=None):
    """
    Return the next scheduled match for the given season.
    If season is not specified, use the current season.

    """
    if not season:
        season = get_current_season()

    meetings = Meetings.objects \
        .order_by('date') \
        .filter(season=season,
                holdout=False,
                date__gte = datetime.date.today())

    mtg = None
    if len(meetings) > 0:
        mtg = meetings[0]

    return mtg


def get_meeting_for_date(date=None):
    """
    Return the meeting object for the specified date.
    """

    season = get_current_season()

    if not date:
        return get_next_meeting(season)

    dt = parser.parse(date)
    meetings = Meetings.objects \
        .filter(season=season,
                holdout=0,
                date__exact = dt.strftime("%Y-%m-%d"))

    if len(meetings) == 1:
        return meetings[0]

    return None


def build_meetings_for_season(force=False):
    """
    Build the meetings for the current season if they don't exist..

    """

    currSeason = get_current_season()
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


def time_to_js(tval):
    """
    Convert a Python time value to the format needed for Javascript.
    """
    return int(time.mktime(tval.timetuple())) * 1000
