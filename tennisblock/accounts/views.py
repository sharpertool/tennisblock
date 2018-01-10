# Create your views here.

from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from TBLib.view import TennisLoginView

class AcccountsLogoutSuccess(TemplateView):
    template_name = 'accounts/logout_success.html'

class AccountsProfile(TennisLoginView):
    template_name = 'accounts/profile.html'

    def get_context_data(self,**kwargs):
        context = super(AccountsProfile, self).get_context_data(**kwargs)
        u = self.request.user
        context['firstname'] = u.first_name
        context['lastname'] = u.last_name
        context['email'] = u.email
        return context

    def post(self,request,*args,**kwargs):
        u = self.request.user
        u.first_name = request.POST['firstname']
        u.last_name = request.POST['lastname']
        u.email = request.POST['email']
        u.save()
        return redirect(reverse('profile'))

class AcccountsLoginSuccess(TemplateView):
    template_name = 'accounts/login_success.html'

class AcccountsDisabled(TemplateView):
    template_name = 'accounts/account_disabled.html'

