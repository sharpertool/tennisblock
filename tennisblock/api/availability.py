import datetime
from django.views.generic.base import View
from rest_framework.parsers import JSONParser
from blockdb.models import Player, SeasonPlayers, Couple, Meetings, Availability, Schedule

from .apiutils import JSONResponse, get_current_season, get_meeting_for_date


def _AvailabilityInit(player, meetings):
    """
    Add blank availability items for the specified player
    """

    for mtg in meetings:
        av = Availability.objects.filter(meeting=mtg, player=player)

        if len(av) == 0:
            av = Availability.objects.create(
                    meeting=mtg,
                    player=player,
                    available=True
            )
            av.save()


class AvailabilityView(View):

    def get_player_data(self, player, mtgs=None, past=None, future=None, single=False):
        """
        Assemble the player data into a structure for the availability index.
        """

        avail = []
        scheduled = []

        # Should be empty arrays if None
        if past is None:
            past =[]
        if future is None:
            future = []

        nplayed = Schedule.objects.filter(meeting__in=past, player=player).count()
        nscheduled = Schedule.objects.filter(meeting__in=future, player=player).count()

        p = {
            'name': player.first + ' ' + player.last,
            'id': player.id,
            'isavail': avail,
            'scheduled': scheduled,
            'nplayed': nplayed,
            'nscheduled': nscheduled + nplayed,
            'single': single
        }

        avlist = Availability.objects.filter(player=player, meeting__in=mtgs).order_by('meeting__date')
        if avlist.count() == 0:
            _AvailabilityInit(player, mtgs)
            avlist = Availability.objects.filter(player=player, meeting__in=mtgs).order_by('meeting__date')

        for idx, mtg in enumerate(mtgs):
            av = avlist[idx]

            avail.append(av.available)
            sch = Schedule.objects.filter(player=player, meeting=mtg)
            scheduled.append(sch.count() > 0)

        return p

    def get(self, request):

        currseason = get_current_season()
        mtgs = Meetings.objects.filter(season=currseason).order_by('date')
        couples = Couple.objects.filter(season=currseason, blockcouple=True).order_by('as_singles')

        past_mtgs = Meetings.objects.filter(season=currseason, date__lte=datetime.date.today())
        future_mtgs = Meetings.objects.filter(season=currseason, date__gt=datetime.date.today())

        pdata = []
        for couple in couples:
            pdata.append(self.get_player_data(couple.male,
                                              single=couple.as_singles, mtgs=mtgs, past=past_mtgs, future=future_mtgs))

            pdata.append(self.get_player_data(couple.female,
                                              single=couple.as_singles, mtgs=mtgs, past=past_mtgs, future=future_mtgs))

        return JSONResponse(pdata)

    def put(self, request):
        # elif request.method == 'PUT':

        data = JSONParser().parse(request)
        currseason = get_current_season()
        mtgs = Meetings.objects.filter(season=currseason).order_by('date')
        try:
            mtg = mtgs[data['mtgidx']]
            p = Player.objects.get(pk=data['id'])
            print("Updating availability for %s on %s to %s" % (p.Name(), mtg.date, data['isavail']))
            av = Availability.objects.get(meeting=mtg, player=p)
            av.available = data['isavail']
            av.save()
        except:
            print("Error trying to update availability")

            # data = request.DATA
        # Update availability for someone.

        return JSONResponse({})
