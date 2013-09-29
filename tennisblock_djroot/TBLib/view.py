# Create your views here.


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class TennisView(TemplateView):

    def get_context_data(self,**kwargs):
        context = super(TennisView, self).get_context_data(**kwargs)
        context['angularapp'] = 'tennisblock'
        context['isLoggedIn'] = self.request.user.is_authenticated()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            print("User is logged in:%s" % request.user.get_full_name())
        else:
            print("user is not logged in")
        return super(TennisView,self).dispatch(request,*args,**kwargs)

class TennisLoginView(TennisView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            print("User is logged in:%s" % request.user.get_full_name())
        else:
            print("user is not logged in")
        return super(TennisLoginView,self).dispatch(request,*args,**kwargs)

