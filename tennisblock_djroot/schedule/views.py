# Create your views here.

from TBLib.view import TennisLoginView


class BlockSchedule(TennisLoginView):
    template_name = "schedule.html"

