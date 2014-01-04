# Create your views here.

from tennisblock.TBLib.view import TennisLoginView

class AvailabilityView(TennisLoginView):
    template_name = "availability.html"

