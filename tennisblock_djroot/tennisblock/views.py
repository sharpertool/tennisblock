# Create your views here.


from django.views.generic import DetailView

from .blockdb.models import *

class HomeView(DetailView):
    template_name = "home.html"
