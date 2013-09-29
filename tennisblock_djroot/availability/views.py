# Create your views here.


from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin

from blockdb.models import *

class AvailabilityView(TemplateView):
    template_name = "availability.html"

    def get_context_data(self,**kwargs):
        context = super(AvailabilityView, self).get_context_data(**kwargs)
        context['angularapp'] = 'tennisblock'
        return context

