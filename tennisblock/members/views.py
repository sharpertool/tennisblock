from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.forms.models import modelformset_factory, inlineformset_factory, BaseModelFormSet
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse

from .forms import UserForm, PlayerForm
from blockdb.models import Player, SeasonPlayer
from api.apiutils import get_current_season
from TBLib.view import TennisLoginView

from members import signals


class PlayerListView(ListView):
    model = Player
    template_name = "members/players.html"
    context_object_name = 'players'


class PlayerDetailView(DetailView):
    queryset = Player.objects.all()
    template_name = "members/player_detail.html"
    context_object_name = 'player'


PlayerUserFormSet = inlineformset_factory(get_user_model(), Player,
                                          fields=(
                                              # 'user.first_name',
                                              # 'user.last_name',
                                              #'first_name',
                                              'gender',
                                              'ntrp',
                                              'microntrp',
                                              'phone',
                                          )
                                      )


class PlayerUpdateView(TemplateView):
    template_name = "members/player_form.html"
    success_url = 'members:player_list'

    def get(self, request, *args, **kwargs):
        #self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Process the results to see if they have been updated.. """
        user_form = UserForm(request.POST)
        player_form = PlayerForm(request.POST)

        if user_form.is_valid() and player_form.is_valid():
            return self.form_valid(user_form, player_form)

    def get_success_url(self):
        return self.success_url

    def form_valid(self, user_form, player_form):
        # signals.player_updated.send(
        #     sender=self.object,
        #     player=self.object,
        #     request=self.request
        # )
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        player_obj = get_object_or_404(Player, pk=kwargs.get('pk', None))
        user_obj = player_obj.user
        context['user_form'] = UserForm(instance=user_obj)
        context['player_form'] = PlayerForm(instance=player_obj)
        return context

    def get_success_url(self):
        return reverse("player_list")


class PlayerCreateView(TemplateView):
    template_name = "members/player_form.html"
    success_url = 'members:player_list'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Process the results to see if they have been updated.. """
        user_form = UserForm(request.POST)
        player_form = PlayerForm(request.POST)

        if user_form.is_valid() and player_form.is_valid():
            return self.form_valid(user_form, player_form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user_form'] = UserForm()
        context['player_form'] = PlayerForm()
        return context

    def form_valid(self, user_form, player_form):
        user_obj = user_form.save()
        player_obj = player_form.save(commit=False)
        player_obj.user = user_obj
        player_obj.save()
        signals.player_created.send(
            sender=player_obj,
            player=player_obj,
            request=self.request
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("player_list")


class PlayerDeleteView(DeleteView):
    model = Player
    template_name = "members/player_confirm_delete.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        signals.player_deleted.send(
            sender=self.object,
            player=self.object,
            request=self.request
        )
        return response

    def get_success_url(self):
        return reverse("player_list")


class PlayersView(TennisLoginView):
    template_name = "players.html"

    def getPlayers(self):
        s = get_current_season()
        sp = Player.objects.all()
        return sp

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get("q")
        if q:
            return queryset.filter(first__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.getPlayers()
        return context


class MembersView(TennisLoginView):
    template_name = "members.html"
    members_only = False

    def getPlayers(self):
        s = get_current_season()
        sp = SeasonPlayer.objects.filter(season=s)
        return [p.player for p in sp if (not self.members_only or p.blockmember)]

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get("q")
        if q:
            return queryset.filter(first__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.getPlayers()
        return context


class SeasonPlayerView(MembersView):
    members_only = True


class SeasonPlayerFormSet(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s = get_current_season()
        self.queryset = Player.objects.all()


class SeasonPlayerFormView(MembersView):
    template_name = "members_form.html"
    members_only = True

    def _get_inline_formset(self, data=None):
        """ Get an inline formset
        """

        AvailFormSet = modelformset_factory(Player)
        # s = get_current_season()
        queryset = Player.objects.all()
        return AvailFormSet(queryset=queryset)

    def _get_formset(self, data=None):
        """ Create the formset object """
        fs = modelformset_factory(Player, formset=SeasonPlayerFormSet)
        return fs

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        PlayerFormSet = self._get_formset()
        fs = PlayerFormSet()
        context['formset'] = fs

        return render(request,
                      self.template_name,
                      context
                      )

    def post(self, request):
        context = self.get_context_data()
        PlayerFormSet = self._get_formset()
        fs = PlayerFormSet(request.POST)

        if fs.is_valid():
            print("Valid Formset!")

            return render(request,
                          self.thankyou_template,
                          context)
        else:
            print("Form is invalid")
            context['formset'] = fs
            return render(request,
                          self.template_name,
                          context
                          )


class SeasonPlayerUpdate(MembersView):
    members_only = True
