from django.shortcuts import render
import datetime

from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView
from blockdb.models import ScheduleVerify, Schedule

from .signals import player_confirmed, player_rejected
from .forms import ScheduleRejectForm


class VerifyMixin:

    @staticmethod
    def get_verify(code):
        try:
            return ScheduleVerify.objects.get(code=code)

        except ScheduleVerify.DoesNotExist:
            pass
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['found'] = False
        if self.verify:
            context['found'] = True
            context['name'] = self.verify.schedule.player.get_full_name()
            context['first'] = self.verify.schedule.player.user.first_name
            context['date'] = self.verify.schedule.meeting.date.strftime(
                "%A, %B %-d")
        return context


class ScheduleConfirmed(VerifyMixin, TemplateView):
    template_name = 'confirm/confirm.html'

    def get(self, request, code=None, **kwargs):
        print(f"Schedule was confirmed with code {code}")
        self.code = code
        self.verify = self.get_verify(code)

        if self.verify is not None:
            player_confirmed.send(self.verify,
                                 player=self.verify.schedule.player,
                                 request=request)

        return super().get(request, **kwargs)


class ScheduleRejected(VerifyMixin, FormView):
    template_name = 'confirm/reject.html'
    form_class = ScheduleRejectForm

    def get_success_url(self):
        return reverse('confirm:reject_done', kwargs={'code': self.code})

    def get(self, request, code=None, **kwargs):
        print(f"Schedule was rejected with code {code}")
        self.code = code
        self.verify = self.get_verify(code)
        return super().get(request, **kwargs)

    def post(self, request, *args, code=None, **kwargs):
        print(f"Post to schedule rejection code {code}")
        self.request = request
        self.code = code
        self.verify = self.get_verify(code)

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        reason = form.cleaned_data.get('reason')
        print(f"Rejected form is valid. We are done. Reason was {reason}")
        player_rejected.send(self.verify,
                    player=self.verify.schedule.player,
                    reason=reason,
                    request=self.request)
        return super().form_valid(form)
    

class ScheduleRejectedComplete(VerifyMixin, TemplateView):
    template_name = 'confirm/rejected.html'

    def get(self, request, code=None, **kwargs):
        self.code = code
        self.verify = self.get_verify(code)
        return super().get(self, request, **kwargs)
