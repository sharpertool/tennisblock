# Create your views here.


from django.views.generic import TemplateView

from blockdb.models import *

class ScheduleView(TemplateView):
    """
    Determine, by default, the next scheduled date for the initial presentation.

    """
    d = {
        #'images'        : images,
        'angularapp'    : 'gardenbuzz',
        #'isprod'        : settings.PROD
    }

    template_name = "schedule.html"
