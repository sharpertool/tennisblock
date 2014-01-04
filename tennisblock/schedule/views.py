# Create your views here.

from tennisblock.TBLib.view import TennisView


class BlockSchedule(TennisView):
    template_name = "schedule.html"

