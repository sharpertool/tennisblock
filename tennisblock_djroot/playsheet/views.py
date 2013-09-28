# Create your views here.


from django.shortcuts import render
from django.views.generic import TemplateView

from blockdb.models import *

class PlaysheetView(TemplateView):
    d = {
        'angularapp'    : 'tennisblock',
    }

    template_name = "playsheet.html"

    def get(self,request):

        return render(request,self.template_name,self.d)

