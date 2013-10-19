# Create your views here.

import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from blockdb.models import Schedule,Couple,Player,SeasonPlayers,Meetings,Availability

from apiutils import JSONResponse, _currentSeason, _getMeetingForDate
from TBLib.teams import TeamManager
from TBLib.schedule import Scheduler

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



@csrf_exempt
def getSubList(request,date=None):

    r = Request(request)

    if r.method == 'GET':
        mtg = _getMeetingForDate(date)

        if mtg:
            data =  {'date' : mtg.date}
        else:
            data = {'date' : None}

        if mtg:

            playingIds = {}
            schedulePlayers = Schedule.objects.filter(meeting=mtg)
            for p in schedulePlayers:
                playingIds[p.player.id] = p.player
                print("Playing this meeting:%s" % p.player.Name())

            avail = Availability.objects.filter(meeting=mtg,available=True)
            fsubs = []
            msubs = []
            for a in avail:
                if not playingIds.has_key(a.player.id):
                    s = {
                        'name' : a.player.Name(),
                        'id'   : a.player.id,
                        'ntrp' : a.player.ntrp,
                        'untrp': a.player.microntrp
                    }

                    if a.player.gender == 'F':
                        fsubs.append(s)
                    else:
                        msubs.append(s)

            others = SeasonPlayers.objects.filter(blockmember=False)
            for sp in others:
                if not playingIds.has_key(sp.player.id):
                    s = {
                        'name' : sp.player.Name(),
                        'id'   : sp.player.id,
                        'ntrp' : sp.player.ntrp,
                        'untrp': sp.player.microntrp
                    }

                    if sp.player.gender == 'F':
                        fsubs.append(s)
                    else:
                        msubs.append(s)

            data['guysubs'] = msubs
            data['galsubs'] = fsubs
        else:
            data['mtg'] = {'error' : 'Could not determine meeting.'}

        return JSONResponse(data)

    return JSONResponse({})

def blockPlayers(request,date=None):

    r = Request(request)

    if r.method == 'GET':
        print("Getting players for block. Requested date:%s" % date)
        tb = Scheduler()
        data = tb.querySchedule(date)
        return JSONResponse(data)

    elif r.method == 'POST':
        data = JSONParser().parse(r)
        couples = data.get('couples')
        result = {'status' : "Did not execute"}
        if couples:
            tb = Scheduler()
            result['status'] = tb.updateSchedule(date,couples)
        else:
            result['status'] = "Did not decode the guys and gals"
        return JSONResponse(result)

    return JSONResponse({})

def getBlockDates(request):
    """
    View function to return a list of the block dates.
    Return the holdout status, and a flag that indicates if the
    meeting is the currently scheduled meeting.
    """

    if request.method == 'GET':
        currSeason = _currentSeason()
        currmtg = _getMeetingForDate()

        meetings = Meetings.objects.filter(season=currSeason).order_by('date')
        mtgData = []
        for mtg in meetings:
            d = {
                'date' : mtg.date,
                'holdout' : mtg.holdout,
                'current' : mtg == currmtg
            }
            mtgData.append(d)

        response = JSONResponse(mtgData)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response


    return JSONResponse({'status' : "Failed"})


@csrf_exempt
def blockSchedule(request,date = None):
    from TBLib.schedule import Scheduler
    tb = Scheduler()

    r = Request(request)

    if r.method == 'GET':
        sched = tb.querySchedule(date)
        return JSONResponse(sched)

    if r.method == 'POST':
        print("blockSchedule POST for date:%s" % date)
        group = tb.getNextGroup()
        print("Groups:")
        for g in group:
            print("\tHe:%s She:%s" % (g.male.Name(),g.female.Name()))

        tb.addCouplesToSchedule(date,group)

        sched = tb.querySchedule(date)

        return JSONResponse(sched)


@csrf_exempt
def getMatchData(request,date = None):

    r = Request(request)

    if r.method == 'GET':
        mgr = TeamManager()

        matchData = mgr.queryMatch(date)
        if matchData:
            return JSONResponse({"match":matchData})
        return JSONResponse({})
