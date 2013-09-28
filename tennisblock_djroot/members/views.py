# Create your views here.


from django.shortcuts import render
from django.views.generic import TemplateView

from blockdb.models import *

class MembersView(TemplateView):
    d = {
        'angularapp'    : 'tennisblock',
    }

    template_name = "members.html"


    def get(self,request):

        return render(request,self.template_name,self.d)
