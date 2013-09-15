# Create your views here.


from django.views.generic import TemplateView

from blockdb.models import *

class HomeView(TemplateView):
    template_name = "home.html"
