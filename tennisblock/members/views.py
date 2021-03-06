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
from TBLib.view import class_login_required

from members import signals

@class_login_required
class PlayerListView(ListView):
    template_name = "members/players.html"
    context_object_name = 'players'
    queryset = Player.objects.all().order_by('user__last_name', 'user__first_name')

@class_login_required
class PlayerDetailView(DetailView):
    queryset = Player.objects.all()
    template_name = "members/player_detail.html"
    context_object_name = 'player'

@class_login_required
class PlayerUpdateView(TemplateView):
    template_name = "members/player_form.html"
    success_url = 'members:player_list'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Process the results to see if they have been updated.. """

        if kwargs.get('pk', None):
            player = Player.objects.get(pk=kwargs.get('pk'))
            user_form = UserForm(request.POST, instance=player.user)
            player_form = PlayerForm(request.POST, instance=player)
        else:
            # Create Method
            user_form = UserForm(request.POST)
            player_form = PlayerForm(request.POST)

        if user_form.is_valid() and player_form.is_valid():
            return self.form_valid(user_form, player_form)

        if not user_form.is_valid():
            return self.form_invalid(user_form)

        if not player_form.is_valid():
            return self.form_invalid(player_form)

        return self.form_invalid(user_form)

    def get_success_url(self):
        return reverse(self.success_url)

    def form_valid(self, user_form, player_form):
        if user_form.changed_data:
            user = user_form.instance
            user.save()

        if player_form.changed_data:
            player = player_form.instance
            player.save()
            signals.player_updated.send(
                sender=player,
                player=player,
                request=self.request
            )

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        player_obj = get_object_or_404(Player, pk=kwargs.get('pk', None))
        user_obj = player_obj.user
        context['player'] = player_obj
        context['user_form'] = UserForm(instance=user_obj)
        context['player_form'] = PlayerForm(instance=player_obj)
        return context

@class_login_required
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
        return reverse(self.success_url)


@class_login_required
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

    def delete(self, request, *args, **kwargs):
        """ Need to delete the user, not the player """
        player = self.get_object()
        success_url = self.get_success_url()
        uid = player.user.pk
        pid = player.id
        player.user.delete()
        print(f"Delete player {pid} and user {uid}")
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse("members:player_list")


@class_login_required
class PlayersView(TennisLoginView):
    template_name = "players.html"

    def get_players(self):
        s = get_current_season()
        sp = Player.objects.all().order_by('last_name', 'first_name')
        return sp

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get("q")
        if q:
            return queryset.filter(first__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.get_players()
        return context


@class_login_required
class MembersViewAngular(TennisLoginView):
    template_name = "members/members_view_angular.html"
    members_only = False

    def get_players(self):
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
        context['players'] = self.get_players()
        return context


@class_login_required
class MembersView(TennisLoginView):
    template_name = "members/members_view.html"
    members_only = False

    def get_players(self):
        s = get_current_season()
        sp = SeasonPlayer.objects.filter(season=s).select_related('player')
        if self.members_only:
            sp.filter(blockmember=True)
        sp.order_by('player__user__last_name', 'player__gender')
        # sp.values('id',
        #           'player__user__first_name', 'player__user__last_name',
        #           'player__gender', 'player__ntrp', 'player__microntrp',
        #           'player__user__email', 'player__phone', 'blockmember')
        return sp

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get("q")
        if q:
            return queryset.filter(first__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.get_players()
        return context


@class_login_required
class MembersViewReact(TennisLoginView):
    template_name = "members/members_view_react.html"

    def get_players(self):
        s = get_current_season()
        sp = SeasonPlayer.objects.filter(season=s).select_related('player')
        sp.order_by('player__user__last_name', 'player__gender')
        return sp

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get("q")
        if q:
            return queryset.filter(first__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.get_players()
        return context


@class_login_required
class SeasonPlayerView(MembersView):
    members_only = True


class SeasonPlayerFormSet(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s = get_current_season()
        self.queryset = Player.objects.all()


@class_login_required
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


@class_login_required
class SeasonPlayerUpdate(MembersView):
    members_only = True
