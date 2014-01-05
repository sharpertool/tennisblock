# Create your views here.

from tennisblock.TBLib.view import TennisView,TennisLoginView

class HomeView(TennisView):
    template_name = "home.html"

class BlockSchedule(TennisLoginView):
    template_name = "schedule.html"

class AvailabilityView(TennisLoginView):
    template_name = "availability.html"

