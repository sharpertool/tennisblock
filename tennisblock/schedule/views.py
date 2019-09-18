from textwrap import dedent
import datetime

from django.views.generic import TemplateView
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle

from TBLib.schedule import Scheduler
from TBLib.season import SeasonManager
from TBLib.view import class_login_required

from .forms import NotifyForm
from .serializers import MeetingSerializer
from blockdb.models import ScheduleVerify, Schedule


@class_login_required
class BlockSchedule(TemplateView):
    """
    display the block schedule for the current, or specified block.

    If the block pk is not specified, use the 'current block'
    """
    template_name = "schedule/index.html"

    def get(self, request, pk=None, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sm = SeasonManager()
        meetings = sm.get_meeting_list()
        serialized = MeetingSerializer(meetings, many=True)
        context['meetings'] = serialized.data
        return context


class ScheduleNotify(TemplateView):
    template_name = "schedule/notify.html"
    thankyou_template = "schedule/thankyou.html"

    def get_couples(self, sch):

        import random

        couples = []
        gals = sch.get('gals')
        guys = sch.get('guys')

        for x in range(0, len(gals)):
            couple = [gals[x].get('name'), guys[x].get('name')]
            random.shuffle(couple)
            couples.append(couple)

        return couples

    def generate_notify_message(self, date, players, extramsg):
        """
        Generate plain text version of message.
        """

        couples = self.get_couples(players)
        cstrings = ["%s and %s" % (c[0], c[1]) for c in couples]
        prefix = "      - "
        msg = dedent("""

            Here is the schedule for Friday, {}:

            {}

            {}

            """.format(date, extramsg, prefix + prefix.join(cstrings)))

        return msg

    def generate_html_notify_message(self, date, players, extramsg):
        """
        Generate an HTML Formatted version of the message.
        """

        couples = self.get_couples(players)
        cstrings = ["<li><span>%s</span> and <span>%s</span></li>"
                    % (c[0], c[1]) for c in couples]

        msg = dedent("""
            <html>
            <head></head>
            <body>
                <h3>Here is the schedule for Friday, %s:</h3>

                %s

                <ul>
                    %s
                </ul>
            </body>
        """ % (date, extramsg, "\n".join(cstrings)))

        return msg

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        date = kwargs.get('date')

        tb = Scheduler()
        if settings.TEST_BLOCK_NOTIFY_RECIPIENTS:
            recipient_list = settings.TEST_BLOCK_NOTIFY_RECIPIENTS
        else:
            recipient_list = tb.get_block_email_list()

        schedule = tb.query_schedule(date)
        context['couples'] = self.get_couples(schedule)
        context['date'] = date

        context['recipients'] = recipient_list
        return context

    def get(self, request, date):
        context = self.get_context_data(date=date)
        form = NotifyForm()

        context['form'] = form
        return render(request,
                      self.template_name,
                      context
                      )

    def post(self, request, date):

        form = NotifyForm(request.POST)

        if form.is_valid():

            extramsg = form.cleaned_data['message']

            tb = Scheduler()

            players = tb.query_schedule(date)

            from_email = settings.EMAIL_HOST_USER

            # Generate Text and HTML versions.
            message = self.generate_notify_message(date, players, extramsg)
            html = self.generate_html_notify_message(date, players, extramsg)

            subject = settings.BLOCK_NOTIFY_SUBJECT % date

            if settings.TEST_BLOCK_NOTIFY_RECIPIENTS:
                recipient_list = settings.TEST_BLOCK_NOTIFY_RECIPIENTS
            else:
                recipient_list = tb.get_block_email_list()

            msg = EmailMultiAlternatives(subject, message, from_email, recipient_list)
            msg.attach_alternative(html, 'text/html')

            print("Message ready to send.. sending.")

            msg.send()

            print("Message sent.")

            return render(request,
                          self.thankyou_template,
                          {'form': form})

        return render(request,
                      self.template_name,
                      {'form': form})


class ScheduleConfirm(APIView):
    throttle_classes = (AnonRateThrottle),
    permission_classes = (AllowAny,)

    def get(self, request, uuid=None):
        """
        Process a uuid code and confirmation type
        Get the confirmation type for the given uuid if found

        Update the schedule with that confirmation type, and then
        remove all ScheduleConfirm objects associated with that schedule item
        """

        try:
            conf = ScheduleVerify.objects.get(code=uuid)
            conf.schedule.confirmation_status = conf.confirmation_type
            conf.schedule.save()

            id = conf.schedule.id

            ScheduleVerify.objects.filter(schedule=conf.schedule).delete()

            if conf.confirmation_type == 'R':
                # Rejected
                return redirect(
                    reverse_lazy('schedule:response_rejected'))
            else:
                return redirect(
                    reverse_lazy('schedule:response_confirmed'))

        except ScheduleVerify.DoesNotExist:
            return HttpResponseBadRequest()


