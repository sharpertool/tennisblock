from textwrap import dedent

from django.views.generic import TemplateView
from django.core.mail import EmailMultiAlternatives

from django.shortcuts import render
from django.conf import settings

from TBLib.schedule import Scheduler
from TBLib.season import SeasonManager
from TBLib.view import class_login_required

from .forms import NotifyForm
from .serializers import MeetingSerializer


@class_login_required
class BlockSchedule(TemplateView):
    """
    Display the block schedule for the current, or specified block.

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

class ScheduleNotify(TemplateView):
    template_name = "schedule/notify.html"
    thankyou_template = "schedule/thankyou.html"

    def getCouples(self, sch):

        import random

        couples = []
        gals = sch.get('gals')
        guys = sch.get('guys')

        for x in range(0, len(gals)):
            couple = [gals[x].get('name'), guys[x].get('name')]
            random.shuffle(couple)
            couples.append(couple)

        return couples

    def generateNotifyMessage(self, date, players, extramsg):
        """
        Generate plain text version of message.
        """

        couples = self.getCouples(players)
        cstrings = ["%s and %s" % (c[0], c[1]) for c in couples]
        prefix = "      - "
        msg = dedent("""

            Here is the schedule for Friday, {}:

            {}

            {}

            """.format(date, extramsg, prefix + prefix.join(cstrings)))

        return msg

    def generateHtmlNotifyMessage(self, date, players, extramsg):
        """
        Generate an HTML Formatted version of the message.
        """

        couples = self.getCouples(players)
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

        context = super(ScheduleNotify, self).get_context_data(**kwargs)

        date = kwargs.get('date')

        tb = Scheduler()
        if settings.BLOCK_NOTIFY_RECIPIENTS:
            recipient_list = settings.BLOCK_NOTIFY_RECIPIENTS
        else:
            recipient_list = tb.getBlockEmailList()

        schedule = tb.querySchedule(date)
        context['couples'] = self.getCouples(schedule)
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

            players = tb.querySchedule(date)

            from_email = settings.EMAIL_HOST_USER

            # Generate Text and HTML versions.
            message = self.generateNotifyMessage(date, players, extramsg)
            html = self.generateHtmlNotifyMessage(date, players, extramsg)

            subject = settings.BLOCK_NOTIFY_SUBJECT % date

            if settings.BLOCK_NOTIFY_RECIPIENTS:
                recipient_list = settings.BLOCK_NOTIFY_RECIPIENTS
            else:
                recipient_list = tb.getBlockEmailList()

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
