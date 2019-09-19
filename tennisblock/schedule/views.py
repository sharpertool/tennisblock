from django.views.generic import TemplateView
from TBLib.season import SeasonManager
from TBLib.view import class_login_required

from .serializers import MeetingSerializer


@class_login_required
class BlockSchedule(TemplateView):
    """
    display the block schedule for the current, or specified block.

    If the block pk is not specified, use the 'current block'
    """
    template_name = "schedule/index.html"

    def get(self, request, pk=None, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sm = SeasonManager()
        meetings = sm.get_meeting_list()
        serialized = MeetingSerializer(meetings, many=True)
        context['meetings'] = serialized.data
        return context


