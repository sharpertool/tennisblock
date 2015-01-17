from textwrap import dedent

from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.views.generic.edit import CreateView

from django.forms.formsets import (
    formset_factory, BaseFormSet)

from django import forms
from django.shortcuts import render
from django.conf import settings
from django.utils.decorators import method_decorator

from TBLib.view import TennisLoginView
from blockdb.models import Season, Meetings, Couple, Player, SeasonPlayers
from forms import ContactForm

from .forms import CoupleForm, AvailabilityForm
from .decorators import login_required
from TBLib.schedule import Scheduler
from TBLib.view import class_login_required

class HomeView(TemplateView):
    template_name = "home.html"


@class_login_required
class AvailabilityView(TemplateView):
    template_name = "availability.html"


class AvailabilityFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(AvailabilityFormSet, self).add_fields(form, index)
        form.field_list = []
        for x in xrange(12):
            f = forms.BooleanField(required=False, label='')
            field_nm = "avail_{}".format(x)
            form.fields[field_nm] = f
            form.field_list.append(field_nm)


@class_login_required
class AvailabilityFormView(TemplateView):
    template_name = "availability_form.html"
    thankyou_template = "thankyou.html"

    def _get_formset(self, data=None):
        """ Create the formset object """
        fs = formset_factory(AvailabilityForm, extra=31, formset=AvailabilityFormSet)
        initial_data = [{'name': 'Billy Bob'}]
        if data:
            return fs(data=data, initial=initial_data)
        return fs(initial=initial_data)

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['formset'] = self._get_formset()

        return render(request, self.template_name, context)

    def post(self, request):
        context = self.get_context_data()
        fs = self._get_formset(data=request.POST)

        if fs.is_valid():
            print("Valid Formset!")

            return render(request,
                          self.thankyou_template,
                          context)
        else:
            print("Form is invalid")
            context['formset'] = fs
            return render(request, self.template_name, context)


@class_login_required
class PlaysheetView(TennisLoginView):
    template_name = "playsheet.html"


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"
    thankyou_template = "thankyou.html"

    def get(self, request):
        form = ContactForm()
        return render(request,
                      self.template_name,
                      {'form': form}
        )

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            from_email = settings.EMAIL_HOST_USER
            recipient_list = settings.CONTACT_FORM_RECIPIENTS

            sender_email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            message = "FROM: %s\n\n\nMESSAGE:\n\n%s" % (sender_email, message)

            subject = settings.CONTACT_FORM_SUBJECT

            send_mail(subject, message, from_email, recipient_list)

            return render(request,
                          self.thankyou_template,
                          {'form': form})

        return render(request,
                      self.template_name,
                      {'form': form})


@class_login_required
class SeasonsView(TemplateView):
    template_name = "seasons.html"

    # queryset = Season.objects.all()

    def get_context_data(self, **kwargs):
        context = super(SeasonsView, self).get_context_data(**kwargs)
        context['seasons'] = Season.objects.all()

        return context

    def get(self, request, pk=None, **kwargs):
        context = self.get_context_data(**kwargs)
        if pk:
            s = Season.objects.filter(pk=pk)
            if s.count():
                context['season'] = s[0]

                context['meetings'] = Meetings.objects.filter(season=s)

        return self.render_to_response(context)


@class_login_required
class SeasonDetailView(TemplateView):
    template_name = "season_detail.html"

    # queryset = Season.objects.all()

    def get(self, request, pk=None, **kwargs):
        context = self.get_context_data(**kwargs)
        if pk:
            s = Season.objects.get(pk=pk)
            context['season'] = s
            context['meetings'] = Meetings.objects.filter(season=s)
            context['players'] = self.get_player_list(s)

        return self.render_to_response(context)

    def get_player_list(self, season):
        """
        Return a list of players and boolean if they are in the given season.

        Set the 'update' flag to false. This is used when updating the values to
        know which players were update to be in the season, and which we can remove.
        """

        players = Player.objects.all().prefetch_related('seasonplayers_set')

        player_data = []
        for p in players:
            player_data.append({
                'pk': p.pk,
                'name': "{} {}".format(p.first, p.last),
                'ntrp': p.ntrp,
                'season_player': p.in_season(season),
                'update': False
            })

        return player_data


    def post(self, request, pk=None, **kwargs):
        context = self.get_context_data(**kwargs)
        if pk:
            s = Season.objects.get(pk=pk)
            meetings = Meetings.objects.filter(season=s)

            if request.POST.get('update_holdouts', False):
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

            context['season'] = s
            context['meetings'] = meetings
            context['players'] = self.get_player_list(s)

        return self.render_to_response(context)

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
                    sp = SeasonPlayers(
                        season=season,
                        player=player,
                        blockmember=True)
                    sp.save()
            elif p['season_player']:
                SeasonPlayers.objects.filter(season=season, player=player).delete()


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

@class_login_required
class CouplesView(TemplateView):
    template_name = "couple_editor.html"

    def get_context_data(self, **kwargs):
        context = super(CouplesView, self).get_context_data(**kwargs)
        return context

    def getcurentcouples(self, context, season):
        players = SeasonPlayers.objects.filter(season=season)
        couples = Couple.objects.filter(season=season)

        context['players'] = players
        context['couples'] = couples
        initial = {
            'season': season.pk,
            'fulltime': False,
            'blockcouple': True,
            'canschedule': True
        }
        context['form'] = CoupleForm(season, initial=initial)

    def get(self, request, pk=None, **kwargs):
        context = self.get_context_data(**kwargs)
        if pk:
            s = Season.objects.filter(pk=pk)
            if s.count():
                season = s[0]
                context['season'] = season

                self.getcurentcouples(context, season)

        return self.render_to_response(context)

    def post(self, request, pk=None, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            s = Season.objects.get(pk=pk)
            context['season'] = s

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
                context['form'] = CoupleForm(s)
            else:
                print("Invalid Couple")
                context['form'] = form

            self.getcurentcouples(context, s)
            return self.render_to_response(context)
        except:
            return self.render_to_response(context)


