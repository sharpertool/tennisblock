# Create your views here.


from django.shortcuts import render
from django.views.generic import TemplateView

from blockdb.models import *

class AvailabilityView(TemplateView):
    template_name = "availability.html"
    d = {
        'angularapp'    : 'tennisblock',
    }


    def get(self,request):

        return render(request,self.template_name,self.d)

