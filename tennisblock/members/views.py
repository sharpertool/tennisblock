from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.forms.models import modelformset_factory, inlineformset_factory, BaseModelFormSet
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse

from .forms import PlayerForm
from blockdb.models import Player, SeasonPlayer
from api.apiutils import get_current_season
from TBLib.view import TennisLoginView

from members import signals


class MemberCreate(CreateView):
    form_class = PlayerForm
    model = Player

    def form_valid(self, form):
        return super(MemberCreate, self).form_valid(form)


class PlayerList(ListView):
    model = Player
    template_name = "members/players.html"
    context_object_name = 'players'


class PlayerDetail(DetailView):
    model = Player
    template_name = "members/player_detail.html"
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlayerDetail, self).get_context_data(**kwargs)
        return context


PlayerUserFormSet = inlineformset_factory(get_user_model(), Player,
                                          fields=('ntrp', 'microntrp', 'phone',))


class PlayerUpdate(UpdateView):
    model = Player
    template_name = "members/player_form.html"
    context_object_name = 'player'
    form_class = PlayerUserFormSet
    fields = ('gender', 'ntrp', 'microntrp', 'phone', )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlayerUpdate, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        response = super(PlayerUpdate, self).form_valid(form)
        signals.player_updated.send(
            sender=self.object,
            player=self.object,
            request=self.request
        )
        return response

    def get_success_url(self):
        return reverse("player_list")


class CreatePlayerView(CreateView):
    model = Player
    template_name = "members/player_form.html"
    form_class = PlayerForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        signals.player_created.send(
            sender=self.object,
            player=self.object,
            request=self.request
        )
        return super(CreatePlayerView, self).form_valid(form)

    def get_success_url(self):
        return reverse("player_list")


class DeletePlayerView(DeleteView):
    model = Player

    def form_valid(self, form):
        response = super(DeletePlayerView, self).form_valid(form)
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
        queryset = super(PlayersView, self).get_queryset()

        q = self.request.GET.get("q")
        if q:
            return queryset.filter(first__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PlayersView, self).get_context_data(**kwargs)
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
        queryset = super(MembersView, self).get_queryset()

        q = self.request.GET.get("q")
        if q:
            return queryset.filter(first__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MembersView, self).get_context_data(**kwargs)
        context['players'] = self.getPlayers()
        return context


class SeasonPlayerView(MembersView):
    members_only = True


class SeasonPlayerFormSet(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super(SeasonPlayerFormSet, self).__init__(*args, **kwargs)
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
