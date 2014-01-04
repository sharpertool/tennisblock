# Create your views here.

from tennisblock.TBLib.view import TennisView,TennisLoginView


class BlockSchedule(TennisLoginView):
    template_name = "schedule.html"

