# Create your views here.

from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from tennisblock.TBLib.view import TennisView,TennisLoginView

from sekizai.context import SekizaiContext

class AccountsLogout(TennisView):
    template_name = 'accounts/logout.html'

    def dispatch(self,request,*args,**kwargs):
        name = ""
        if request.user.is_authenticated():
            name = request.user.get_full_name()
        logout(request)

        # Redirect to a success page
        return redirect(reverse('login-success'))

class AcccountsLogoutSuccess(TennisView):
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

class AccountsLogin(TennisView):
    template_name = 'accounts/login.html'

    def get_context_data(self,**kwargs):
        context = super(TennisView, self).get_context_data(**kwargs)
        return context

    def get(self,request,*args,**kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self,request,*args,**kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                next = request.POST['next']
                if next:
                    return redirect(next)
                else:
                    return redirect(reverse('login-success'))
            else:
                return redirect(reverse('account-disabled'))
        else:
            kwargs['message'] = "Invalid Login Credentials"
            return redirect(reverse('login'))

class AcccountsLoginSuccess(TennisView):
    template_name = 'accounts/login_success.html'

class AcccountsDisabled(TennisView):
    template_name = 'accounts/account_disabled.html'

