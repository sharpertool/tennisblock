# Create your views here.


from django.views.generic import TemplateView

from blockdb.models import *

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self,**kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['angularapp'] = 'tennisblock'
        return context

