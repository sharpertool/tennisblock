# Create your views here.


from django.shortcuts import render
from django.views.generic import TemplateView


class BlockSchedule(TemplateView):
    """
    Determine, by default, the next scheduled date for the initial presentation.

    """
    d = {
        'angularapp'    : 'tennisblock',
    }

    template_name = "schedule.html"

    def get(self,request):

        return render(request,self.template_name,self.d)

