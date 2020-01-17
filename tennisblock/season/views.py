from crispy_forms.layout import Submit
from dateutil.parser import parse
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db import models
from django.db.models.expressions import Value, F, Q
from django.db.models.functions import Concat

from TBLib.view import class_login_required

from blockdb.models import Season, Meeting, Player, SeasonPlayer, Couple

from .forms import SeasonForm, CoupleForm
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

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

    def post(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is not None:
            s = Season.objects.get(pk=pk)

            if request.POST.get('update_season', False):
                season_form = SeasonForm(request.POST,
                                         instance=s)
                if season_form.is_valid():
                    season_form.save()
                else:
                    context = self.get_context_data(
                        season_form=season_form)
                    return self.render_to_response(context)
            elif request.POST.get('update_holdouts', False):
                meetings = Meeting.objects.filter(season=s).order_by('date')
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
        pk = kwargs.get('pk')
        if pk is not None:
            s = Season.objects.get(pk=pk)
            context['season'] = s
            if kwargs.get('season_form') is None:
                context['season_form'] = SeasonForm(instance=s)
                context['season_form'].helper.add_input(
                    Submit('update_season', 'Update Season')
                )

            meetings = Meeting.objects.filter(season=s).order_by('date')
            if len(meetings) == 0:
                build_meetings_for_season(s)
                meetings = Meeting.objects.filter(season=s).order_by('date')
            context['meetings'] = meetings
            context['active'] = self.active_season_players(s)
            context['inactive'] = self.non_season_players(s)

        return context

    def active_season_players(self, season):
        sqs = Season.objects.filter(pk=season.pk)

        active = Player.objects \
            .filter(Q(seasons__in=sqs)) \
            .annotate(active=Value(True, models.BooleanField())) \
            .annotate(uname=Concat('user__last_name',
                                   Value(', '),
                                   'user__first_name'))

        return active.order_by('uname')

    def non_season_players(self, season):
        sqs = Season.objects.filter(pk=season.pk)

        inactive = Player.objects \
            .filter(~Q(seasons__in=sqs)) \
            .annotate(active=Value(False, models.BooleanField())) \
            .annotate(uname=Concat('user__last_name',
                                   Value(', '),
                                   'user__first_name'))

        return inactive.order_by('uname')

    def update_season_players(self, season, request):
        player_keys = [int(k) for k in request.POST.getlist('members')]

        print(f"Keys: {sorted(player_keys)}")

        sel_players = Player.objects.filter(pk__in=player_keys).order_by('pk')
        curr_players = Player.objects.filter(Q(seasons__in=[season])).order_by('pk')

        print(f"Selected: {sel_players.all().values_list('pk')}")
        print(f"Current: {curr_players.all().values_list('pk')}")

        to_del = curr_players.difference(sel_players).order_by('pk')
        to_add = sel_players.difference(curr_players).order_by('pk')

        for p in to_del.all():
            print(f"Deleting {p}")
            SeasonPlayer.objects.get(season=season, player=p).delete()

        for p in to_add.all():
            print(f"Adding {p}")
            SeasonPlayer.objects.create(
                season=season,
                player=p,
                blockmember=True
            ).save()


@class_login_required
class SeasonCreate(CreateView):
    template_name = "season/season_create.html"
    success_url = reverse_lazy('season:seasons')
    form_class = SeasonForm
    model = Season

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].helper.add_input(
            Submit('submit', 'Create Season')
        )
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@class_login_required
class CouplesView(TemplateView):
    template_name = "season/couple_editor.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)

        season = get_object_or_404(Season, pk=pk)
        context['season'] = season

        players = SeasonPlayer.objects.filter(season=season)
        couples = Couple.objects.filter(season=season)

        context['players'] = players
        context['couples'] = couples
        initial = {
            'season': season,
            'fulltime': False,
            'blockcouple': True,
            'canschedule': True
        }
        context['form'] = CoupleForm(season, initial=initial)

        return context

    def get(self, request, pk=None, **kwargs):
        context = self.get_context_data(pk=pk, **kwargs)
        return self.render_to_response(context)

    def post(self, request, pk=None, **kwargs):

        try:
            s = get_object_or_404(Season, pk=pk)

            form = CoupleForm(s, request.POST)
            if form.is_valid():
                print("Valid Couple form..updating...")
                Couple.objects.create(
                    season=s,
                    name=form.data['name'],
                    male=form.spguy.player,
                    female=form.spgal.player,
                    fulltime=form.data.get('fulltime', 'off') == 'on',
                    blockcouple=form.data.get('blockcouple', 'off') == 'on',
                    canschedule=True
                ).save()
                print("Inserted couple")
            else:
                print("Invalid Couple")

        except IntegrityError:
            print("Attempt to insert duplicate couple!")

        context = self.get_context_data(pk=pk, **kwargs)
        return self.render_to_response(context)

    def insert_couple(self, couple=None):
        """ Check for duplicates before inserting """
        if not Couple.objects.filter(
                male=couple.male,
                female=couple.female, season=couple.season).exists():
            couple.save()
