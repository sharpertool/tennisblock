from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


def class_login_required(View):
    View.dispatch = method_decorator(login_required)(View.dispatch)
    return View


class TennisLoginView(TemplateView):
    """
    Base class for tennis views that require login
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TennisLoginView, self).dispatch(request, *args, **kwargs)
