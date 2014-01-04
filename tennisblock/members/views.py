# Create your views here.


from tennisblock.TBLib.view import TennisView, TennisLoginView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from tennisblock.blockdb.models import Player,SeasonPlayers
from forms import PlayerForm

from tennisblock.api.apiutils import _currentSeason

class MemberCreate(CreateView):
    form_class = PlayerForm
    model = Player

    def form_valid(self,form):
        return super(MemberCreate,self).form_valid(form)

class MembersView(TennisLoginView):
    template_name = "members.html"
    members_only = False

    def getPlayers(self):
        s = _currentSeason()
        sp = SeasonPlayers.objects.filter(season = s)
        return [p.player for p in sp if (not self.members_only or p.blockmember)]

    def get_queryset(self):
        queryset =super(MembersView,self).get_queryset()

        q = self.request.GET.get("q")
        if q:
            return queryset.filter(first__icontains=q)
        return queryset

    def get_context_data(self,**kwargs):
        context = super(MembersView, self).get_context_data(**kwargs)
        context['players'] = self.getPlayers()
        return context


class SeasonPlayersView(MembersView):
    members_only = True

