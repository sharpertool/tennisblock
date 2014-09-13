
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.forms.models import modelformset_factory,BaseModelFormSet
from django.forms.models import inlineformset_factory

from forms import PlayerForm
from blockdb.models import Player,SeasonPlayers
from api.apiutils import get_current_season
from TBLib.view import TennisLoginView

class MemberCreate(CreateView):
    form_class = PlayerForm
    model = Player

    def form_valid(self,form):
        return super(MemberCreate,self).form_valid(form)

class MembersView(TennisLoginView):
    template_name = "members.html"
    members_only = False

    def getPlayers(self):
        s = get_current_season()
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

class SeasonPlayersFormSet(BaseModelFormSet):

    def __init__(self,*args,**kwargs):
        super(SeasonPlayersFormSet,self).__init__(*args,**kwargs)
        s = get_current_season()
        self.queryset = SeasonPlayers.objects.filter(season = s)

class SeasonPlayersFormView(MembersView):
    template_name = "members_form.html"
    members_only = True

    def _get_inline_formset(self,data=None):
        """ Get an inline formset
        """

        AvailFormSet = inlineformset_factory(Player,SeasonPlayers)
        s = get_current_season()
        queryset = SeasonPlayers.objects.filter(season = s)
        return AvailFormSet(queryset=queryset)

    def _get_formset(self,data=None):
        """ Create the formset object """
        fs = modelformset_factory(SeasonPlayers,formset=SeasonPlayersFormSet)
        return fs()

    def get(self,request,**kwargs):
        context = self.get_context_data(**kwargs)
        context['formset'] = self._get_inline_formset()

        return render(request,
                      self.template_name,
                      context
        )

    def post(self,request):
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
            return render(request,
                          self.template_name,
                          context
            )


class SeasonPlayersUpdate(MembersView):
    members_only = True
