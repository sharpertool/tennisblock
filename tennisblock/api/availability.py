import datetime
from django.views.generic.base import View
from rest_framework.parsers import JSONParser
from blockdb.models import Player, Couple, Meeting, Availability, Schedule, SeasonPlayer, PlayerAvailability

from .apiutils import JSONResponse, get_current_season


def _AvailabilityInit(player, meetings):
    """
    Add blank availability items for the specified player
    """

    for mtg in meetings:
        try:
            Availability.objects.get(meeting=mtg, player=player)

        except Availability.DoesNotExist:
            Availability.objects.create(
                meeting=mtg,
                player=player,
                available=True
            ).save()


class AvailabilityView(View):

    def get_player_data(self, player, season, mtgs=None, past=None, future=None, single=False):
        """
        Assemble the player data into a structure for the availability index.
        """

        avail = []
        scheduled = []

        # Should be empty arrays if None
        if past is None:
            past = []
        if future is None:
            future = []

        nplayed = Schedule.objects.filter(meeting__in=past, player=player).count()
        nscheduled = Schedule.objects.filter(meeting__in=future, player=player).count()

        av = PlayerAvailability.objects.get_for_season_player(player, season)

        p = {
            'name': player.first + ' ' + player.last,
            'id': player.id,
            'isavail': av.available,
            'scheduled': av.scheduled,
            'nplayed': nplayed,
            'nscheduled': nscheduled + nplayed,
            'single': single
        }

        return p

    def get(self, request):

        currseason = get_current_season()
        mtgs = Meeting.objects.filter(season=currseason).order_by('date')
        availability_count = len(mtgs)
        couples = Couple.objects.filter(season=currseason, blockcouple=True).order_by('as_singles')

        season_players = SeasonPlayer.objects.filter(
            season=currseason)

        past_mtgs = Meeting.objects.filter(season=currseason, date__lte=datetime.date.today())
        future_mtgs = Meeting.objects.filter(season=currseason, date__gt=datetime.date.today())

        pdata = []
        for sp in season_players:
            pdata.append(self.get_player_data(sp.player,
                                              currseason,
                                              mtgs=mtgs,
                                              past=past_mtgs,
                                              future=future_mtgs))

        return JSONResponse(pdata)

    def put(self, request):
        # elif request.method == 'PUT':

        data = JSONParser().parse(request)
        index = data['mtgidx']
        available = data['isavail']
        currseason = get_current_season()
        player = Player.objects.get(pk=data['id'])
        av = PlayerAvailability.objects.get_for_season_player(player, currseason)

        response = {'status': 'success'}
        if index < len(av.available):
            av.available[index] = available
            av.save()
        else:
            response = {'status': 'failed', 'msg': 'index out of range'}

        return JSONResponse(response)
