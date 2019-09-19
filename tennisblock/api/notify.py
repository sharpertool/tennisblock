import random
import datetime
from textwrap import dedent
from django.views.generic.base import View
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.template import loader
from django.shortcuts import redirect
from django.db.models import Q, ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import authentication, permissions
from blockdb.models import Schedule, Couple, Player, SeasonPlayer, Meeting, Availability, PlayerAvailability, \
    ScheduleVerify

from .apiutils import JSONResponse, get_current_season, get_meeting_for_date, time_to_js
from TBLib.manager import TeamManager
from TBLib.schedule import Scheduler

from confirm.signals import player_rejected, player_confirmed


class BlockNotifierMixin:
    html_template = 'api/block_schedule_update.html'
    text_template = 'api/block_schedule_update.txt'

    @staticmethod
    def build_player_list(players):
        playerlist = []

        gals = players.get('gals')
        guys = players.get('guys')

        for x in range(0, len(gals)):
            couple = [gals[x], guys[x]]
            random.shuffle(couple)
            playerlist.append((couple[0].get('name'), couple[1].get('name'),))

        return playerlist

    def build_notify_message(self, date, players, message=None):
        """
        Generate plain text version of message.
        """
        playerlist = self.build_player_list(players)

        context = {
            'players': playerlist,
            'date': date.strftime('%A, %B %-d'),
            'message': message,
        }

        text_template = loader.get_template(self.text_template)
        rendered = text_template.render(context)

        return rendered

    def build_html_notify_message(self, date, players, message=None):
        """
        Generate an HTML Formatted version of the message.
        """

        playerlist = self.build_player_list(players)
        context = {
            'players': playerlist,
            'date': date.strftime('%A, %B %-d'),
            'message': message,
        }

        html_template = loader.get_template(self.html_template)
        rendered = html_template.render(context)

        return rendered

    def send_schedule_update(self, request, date, message=None):
        tb = Scheduler()

        mtg = get_meeting_for_date(date)
        players = tb.query_schedule(date)

        from_email = settings.EMAIL_HOST_USER

        # Generate Text and HTML versions.
        body = self.build_notify_message(mtg.date, players, message=message)
        html_body = self.build_html_notify_message(mtg.date, players, message=message)

        subject = settings.BLOCK_NOTIFY_SUBJECT % date

        if settings.TEST_BLOCK_NOTIFY_RECIPIENTS:
            recipients = settings.TEST_BLOCK_NOTIFY_RECIPIENTS
            cc_list = []
        else:
            recipients, cc_list = tb.get_notify_email_lists()

        msg = EmailMultiAlternatives(subject=subject,
                                     body=body,
                                     from_email=from_email,
                                     to=recipients,
                                     cc=cc_list)
        msg.attach_alternative(html_body, 'text/html')

        msg.send()

        return JSONResponse({})

    @property
    def ignore_emails(self):
        ignore_emails = []
        if settings.NOTIFY_FORCE_EMAIL:
            ignore_emails += settings.NOTIFY_FORCE_EMAIL

        if settings.TEST_BLOCK_NOTIFY_RECIPIENTS:
            ignore_emails += settings.TEST_BLOCK_NOTIFY_RECIPIENTS[0]
        return ignore_emails

    def verify_player(self, request, meeting, player):

        verify = player.get_verification()
        if verify.confirmation_type != 'C':
            if verify.sent_on is None:
                verify.sent_on = timezone.now()
                verify.sent_to = player.player.user.email
            verify.received_on = timezone.now()
            verify.confirmation_type = 'C'
            verify.save()

    def notify_player(self, request, meeting,
                      message, scheduled_player,
                      ignore_emails=None, force=False):
        ignore_emails = [] if ignore_emails is None else ignore_emails

        email = scheduled_player.player.user.email

        verify = scheduled_player.get_verification()

        should_send = any([
            force,
            verify.sent_on is None,
            all([
                verify.sent_to is not None,
                verify.sent_to != '',
                email != verify.sent_to,
                verify.sent_to in ignore_emails,
            ])
        ])

        if should_send:
            print(f'Time to send a notification to {verify.code}')
            verify.email = email
            sent_to = verify.send_verify_request(
                request,
                date=meeting.date,
                message=message,
                force_to=settings.TEST_BLOCK_NOTIFY_RECIPIENTS
            )
            verify.sent_on = timezone.now()
            verify.sent_to = sent_to
            verify.confirmation_type = 'A'
            verify.save()


class ScheduleNotifyView(BlockNotifierMixin, APIView):

    def get(self, request, date=None):
        mtg = get_meeting_for_date(date)
        sch = Schedule.objects.filter(meeting=mtg)
        sch = sch.select_related('player').select_related('verification')

        def vtype(s):
            v = s.get_verification()
            if v:
                return v.confirmation_type
            return ''

        schdata = [
            (s.player.id,
             vtype(s),)
            for s in sch.all()
        ]
        results = {}
        for data in schdata:
            results[data[0]] = data[1]

        return Response({
            "status": "success",
            "results": results
        })

    def post(self, request, date=None):
        """
        Send a notification to all scheduled players for the given date

        ToDo:
            - Send request if created
            - Remove existing ScheduleVerify objects if player was removed
              from the schedule
            - Ignore a verification if a person clicks on an out-of-date
              verification
        """
        message = request.data.get('message')
        print(f"Message to home: {message}")

        mtg = get_meeting_for_date(date)
        scheduled_players = Schedule.objects.filter(
            meeting=mtg
        ).select_related('player').select_related('verification')

        for scheduled_player in scheduled_players:
            self.notify_player(request, mtg, message,
                               scheduled_player, self.ignore_emails)

        self.send_schedule_update(request, date, message=message)

        return Response({"status": "success"})


class PlayerNotifyView(BlockNotifierMixin, APIView):

    def post(self, request, player_id=None):
        mtg = get_meeting_for_date()
        player = get_object_or_404(Schedule,
                                   meeting=mtg,
                                   player__id=player_id)

        self.notify_player(request, mtg, '',
                           player,
                           ignore_emails=self.ignore_emails,
                           force=True)
        return Response({"status": "success"})


class PlayerVerifyView(BlockNotifierMixin, APIView):

    def post(self, request, player_id=None):
        mtg = get_meeting_for_date()
        player = get_object_or_404(Schedule,
                                   meeting=mtg,
                                   player__id=player_id)
        self.verify_player(request, mtg, player)
        return Response({"status": "success"})
