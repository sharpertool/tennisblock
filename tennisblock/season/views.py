from dateutil.parser import parse
from django.views.generic import TemplateView, CreateView

from TBLib.view import class_login_required

from blockdb.models import Season, Meeting, Player, SeasonPlayer

from .forms import SeasonForm
from api.apiutils import build_meetings_for_season

@class_login_required
class SeasonsView(TemplateView):
    template_name = "season/seasons.html"

    # queryset = Season.objects.all()

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seasons'] = Season.objects.all()
        pk = kwargs.get('pk', None)
        if pk is not None:
            s = Season.objects.filter(pk=pk)
            if s.count():
                context['season'] = s[0]

                context['meetings'] = Meeting.objects.filter(season=s)

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, *args, **kwargs)

        return self.render_to_response(context)


@class_login_required
class SeasonDetailView(TemplateView):
    template_name = "season/season_detail.html"

    # queryset = Season.objects.all()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

    def post(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is not None:
            s = Season.objects.get(pk=pk)
            meetings = Meeting.objects.filter(season=s)

            if request.POST.get('update_season', False):
                print("Update Season data..")
                p = request.POST
                # s.blocktime = p.get('blocktime')
                s.courts = p.get('courts')
                s.firstcourt = p.get('firstcourt')
                s.name = p.get('name')
                s.enddate = parse(p.get('seasonend'))
                s.startdate = parse(p.get('seasonstart'))
                s.blockstart = parse(p.get('blockstart'))
                s.save()
            elif request.POST.get('update_holdouts', False):
                holdouts = request.POST.getlist('meetings')
                for m in meetings:
                    m.holdout = False
                for h in holdouts:
                    h = int(h)
                    meetings[h].holdout = True
                for m in meetings:
                    m.save()

            elif request.POST.get('season_players', False):
                self.update_season_players(s, request)

            context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk', None)
        if pk is not None:
            s = Season.objects.get(pk=pk)
            context['season'] = s
            context['season_form'] = SeasonForm(instance=s)
            meetings = Meeting.objects.filter(season=s)
            if len(meetings) == 0:
                build_meetings_for_season(s)
                meetings = Meeting.objects.filter(season=s)
            context['meetings'] = meetings
            context['players'] = self.get_player_list(s)

        return context


    def get_player_list(self, season):
        """
        Return a list of players and boolean if they are in the given season.

        Set the 'update' flag to false. This is used when updating the values to
        know which players were update to be in the season, and which we can remove.
        """

        players = Player.objects.all().prefetch_related('seasonplayer_set')

        player_data = []
        for p in players:
            player_data.append({
                'pk': p.pk,
                'name': "{} {}".format(p.first, p.last),
                'ntrp': p.ntrp,
                'season_player': p.in_season(season),
                'block_member': False,
                'update': False
            })

        return player_data

    def update_season_players(self, season, request):
        player_keys = request.POST.getlist('members')

        all_players = self.get_player_list(season)
        for idx in player_keys:
            idx = int(idx)
            player = all_players[idx]
            player['update'] = True

        for p in all_players:
            player = Player.objects.get(pk=p['pk'])
            if p['update']:
                if not p['season_player']:
                    sp = SeasonPlayer(
                        season=season,
                        player=player,
                        blockmember=True)
                    sp.save()
            elif p['season_player']:
                SeasonPlayer.objects.filter(season=season, player=player).delete()


@class_login_required
class SeasonCreate(CreateView):
    model = Season
    fields = [
        'name',
        'courts',
        'firstcourt',
        'startdate',
        'enddate',
        'blockstart',
        'blocktime'
    ]
