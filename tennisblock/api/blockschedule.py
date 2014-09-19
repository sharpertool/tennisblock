# Create your views here.

import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from blockdb.models import Schedule,Couple,Player,SeasonPlayers,Meetings,Availability

from .apiutils import JSONResponse, get_current_season, get_meeting_for_date,time_to_js
from TBLib.teams import TeamManager
from TBLib.schedule import Scheduler

def _BuildMeetings(force=False):
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
                'him' : c.male.user.first_name + ' ' + c.male.user.last_name,
                'her' : c.female.user.first_name + ' ' + c.female.user.last_name
            }
            data.append(d)

        return JSONResponse(data)



@csrf_exempt
def getSubList(request,date=None):

    r = Request(request)

    if r.method == 'GET':
        mtg = get_meeting_for_date(date)

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
            mgr = TeamManager()
            mgr.dbTeams.deleteMatchup(date)
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
        currSeason = get_current_season()
        currmtg = get_meeting_for_date()

        meetings = Meetings.objects.filter(season=currSeason).order_by('date')
        mtgData = []
        for mtg in meetings:
            jstime = time_to_js(mtg.date)
            d = {
                'date' : mtg.date,
                'holdout' : mtg.holdout,
                'current' : mtg == currmtg
            }
            mtgData.append(d)

        response = JSONResponse(mtgData)
        return response


    return JSONResponse({'status' : "Failed"})


@csrf_exempt
def blockSchedule(request,date = None):
    from  TBLib.schedule import Scheduler
    tb = Scheduler()

    r = Request(request)

    if r.method == 'GET':
        sched = tb.querySchedule(date)
        return JSONResponse(sched)

    if r.method == 'POST':
        print("blockSchedule POST for date:%s" % date)
        group = tb.getNextGroup(date)
        print("Groups:")
        for g in group:
            print("\tHe:%s She:%s" % (g.male.Name(),g.female.Name()))

        tb.addCouplesToSchedule(date,group)

        mgr = TeamManager()
        mgr.dbTeams.deleteMatchup(date)

        sched = tb.querySchedule(date)

        return JSONResponse(sched)

    if r.method == 'DELETE':
        print("blockSchedule DELETE for date:%s" % date)
        mgr = TeamManager()
        mgr.dbTeams.deleteMatchup(date)
        tb.removeAllCouplesFromSchedule(date)

        return JSONResponse({})

@csrf_exempt
def getMatchData(request,date = None):

    r = Request(request)

    if r.method == 'GET':
        mgr = TeamManager()

        matchData = mgr.queryMatch(date)
        if matchData:
            return JSONResponse({"match":matchData})
        return JSONResponse({})

class BlockNotifyer(View):

    def generateNotifyMessage(self,date,players):
        """
        Generate plain text version of message.
        """

        import random
        playerList = []
        prefix = "      - "

        gals = players.get('gals')
        guys = players.get('guys')

        for x in range(0,len(gals)):
            couple = [gals[x],guys[x]]
            random.shuffle(couple)
            playerList.append("%s and %s" % (couple[0].get('name'),couple[1].get('name')))
        msg = """
=

Here is the schedule for Friday, %s:
%s

        """ % (date,prefix + prefix.join(playerList))

        return msg

    def generateHtmlNotifyMessage(self,date,players):
        """
        Generate an HTML Formatted version of the message.
        """

        import random
        playerList = []

        gals = players.get('gals')
        guys = players.get('guys')

        for x in range(0,len(gals)):
            couple = [gals[x],guys[x]]
            random.shuffle(couple)
            playerList.append("<li><span>%s</span> and <span>%s</span></li>" % (couple[0].get('name'),couple[1].get('name')))
        msg = """

        <html>
        <head></head>
        <body>
            <h3>Here is the schedule for Friday, %s:</h3>

        <ul>
            %s
        </ul>

        """ % (date,"\n".join(playerList))

        return msg

    def post(self, request,date):
        tb = Scheduler()

        players = tb.querySchedule(date)

        from_email = settings.EMAIL_HOST_USER

        # Generate Text and HTML versions.
        message = self.generateNotifyMessage(date,players)
        html = self.generateHtmlNotifyMessage(date,players)

        subject = settings.BLOCK_NOTIFY_SUBJECT % date

        if settings.BLOCK_NOTIFY_RECIPIENTS:
            recipient_list = ['ed@tennisblock.com','viquee@me.com']
        else:
            recipient_list = tb.getBlockEmailList()

        msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        msg.attach_alternative(html,'text/html')

        msg.send()

        return JSONResponse({})

