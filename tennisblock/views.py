# Create your views here.

from tennisblock.TBLib.view import TennisView,TennisLoginView

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
