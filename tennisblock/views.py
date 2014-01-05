# Create your views here.

from tennisblock.TBLib.view import TennisView,TennisLoginView
from tennisblock.blockdb.models import Season,Meetings

class HomeView(TennisView):
    template_name = "home.html"

class BlockSchedule(TennisLoginView):
    template_name = "schedule.html"

class AvailabilityView(TennisLoginView):
    template_name = "availability.html"

class PlaysheetView(TennisView):
    template_name = "playsheet.html"

class AboutView(TennisView):
    template_name = "about.html"

class ContactView(TennisView):
    template_name = "contact.html"

class SeasonsView(TennisLoginView):
    template_name = "seasons.html"

    #queryset = Season.objects.all()

    def get_context_data(self,**kwargs):
        context = super(SeasonsView,self).get_context_data(**kwargs)
        context['seasons'] = Season.objects.all()

        return context

    def get(self,request,name=None, **kwargs):
        context = self.get_context_data(**kwargs)
        if name:
            s = Season.objects.filter(name__icontains=name)
            if s.count():
                context['season'] = s[0]

                context['meetings'] = Meetings.objects.filter(season=s)

        return self.render_to_response(context)



