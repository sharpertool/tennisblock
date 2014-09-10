from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class TennisLoginView(TemplateView):
    """
    Base class for tennis views that require login
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TennisLoginView,self).dispatch(request,*args,**kwargs)

