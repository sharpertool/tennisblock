import random
import datetime
from textwrap import dedent
from django.views.generic.base import View
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
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

def _BuildMeetings(force=False):
    """
    Build the meetings for the current season if they don't exist..

    """

    current_season = get_current_season()
    if not current_season:
        return

    current_season.ensure_meetings_exist(recreate=force)


def _AvailabilityInit(player, meetings):
    """
    Add blank availability items for the specified player
    """

    for mtg in meetings:
        av = Availability.objects.filter(meeting=mtg, player=player)

        if len(av) == 0:
            av = Availability.objects.create(
                meeting=mtg,
                player=player,
                available=True
            )
            av.save()


class SubsView(APIView):

    def get(self, request, format=None, date=None):
        mtg = get_meeting_for_date(date)
        # print(f"Date: {date} Meeting:{mtg}")
        if mtg:
            data = {'date': mtg.date}
        else:
            data = {'date': None}

        if mtg:

            mtg_index = mtg.meeting_index

            playingIds = {}
            schedulePlayers = Schedule.objects.filter(meeting=mtg)
            for p in schedulePlayers:
                playingIds[p.player.id] = p.player
                # print("Playing this meeting:%s" % p.player.Name())

            subs = PlayerAvailability.objects.filter(~Q(player__in=playingIds))
            subs = subs.filter(**{f'available__{mtg_index}': True})

            fsubs = []
            msubs = []

            for p in subs:
                s = {
                    'name': p.player.Name(),
                    'id': p.player.id,
                    'ntrp': p.player.ntrp,
                    'untrp': p.player.microntrp,
                    'gender': p.player.gender.lower()
                }

                fsubs.append(s) if p.player.gender == 'F' else msubs.append(s)

            others = SeasonPlayer.objects.filter(
                blockmember=False,
                season=mtg.season
            ).filter(
                ~Q(player__in=playingIds)
            )

            for p in others:
                s = {
                    'name': p.player.Name(),
                    'id': p.player.id,
                    'ntrp': p.player.ntrp,
                    'untrp': p.player.microntrp,
                    'gender': p.player.gender.lower()
                }

                fsubs.append(s) if p.player.gender == 'F' else msubs.append(s)

            data['guysubs'] = msubs
            data['galsubs'] = fsubs
        else:
            data['mtg'] = {'error': 'Could not determine meeting.'}

        return Response(data)


class BlockPlayers(APIView):
    http_method_names = ['get', 'post', 'head', 'options']
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, date=None):
        print(f"Getting players for block for date {date}")
        tb = Scheduler()
        data = tb.query_schedule(date)
        return Response(data)

    def post(self, request, date=None):
        couples = request.data.get('couples')
        result = {'status': "Did not execute"}

        if couples:
            tb = Scheduler()
            result['status'] = tb.update_schedule(date, couples)
            mgr = TeamManager()
            mgr.dbTeams.delete_matchup(date)
        else:
            result['status'] = "Did not decode the guys and gals"
        return Response(result)


class BlockDates(APIView):
    http_method_names = ['get', 'head', 'options']
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        curr_season = get_current_season()
        current_meeting = get_meeting_for_date()

        court_count = curr_season.courts

        meetings = Meeting.objects.filter(
            season=curr_season).order_by('date')
        result = []
        for mtg in meetings:
            d = {
                'date': mtg.date,
                'holdout': mtg.holdout,
                'current': mtg == current_meeting,
                'num_courts': court_count
            }
            if mtg.court_count:
                d['num_courts'] = mtg.court_count

            result.append(d)

        return Response(result)


class BlockSchedule(APIView):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, date=None):
        tb = Scheduler()
        sched = tb.query_schedule(date)
        return Response(sched)

    def post(self, request, date=None):
        # ToDo: Insure is Admin user, not just authenticated
        tb = Scheduler()
        print("blockSchedule POST for date:%s" % date)
        group = tb.get_next_group(date)
        print("Groups:")
        for g in group:
            print("\tHe:%s She:%s" % (g.male.Name(), g.female.Name()))

        tb.add_couples_to_schedule(date, group)

        mgr = TeamManager()
        mgr.dbTeams.delete_matchup(date)

        sched = tb.query_schedule(date)

        return Response(sched)

    def delete(self, request, date=None):
        # ToDo: Insure is Admin user, not just authenticated
        tb = Scheduler()
        print("blockSchedule DELETE for date:%s" % date)
        mgr = TeamManager()
        mgr.dbTeams.delete_matchup(date)
        tb.remove_all_couples_from_schedule(date)
        return Response({'status': 'success'})


class MatchData(APIView):
    def get(self, request, date=None):
        mgr = TeamManager()

        matchData = mgr.query_match(date)
        if matchData:
            return Response({"match": matchData})
        return Response({})


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
              verifiation
        """
        message = request.data.get('message')
        print(f"Message to home: {message}")

        mtg = get_meeting_for_date(date)
        scheduled_players = Schedule.objects.filter(
            meeting=mtg
        ).select_related('player').select_related('verification')

        email_list = []
        for scheduled_player in scheduled_players:
            email = scheduled_player.player.user.email

            verify = scheduled_player.get_verification()

            should_send = any([
                verify.sent_on is None,
                all([
                    verify.sent_to is not None,
                    verify.sent_to != '',
                    email != verify.sent_to,
                    verify.sent_to != settings.NOTIFY_FORCE_EMAIL,
                    verify.sent_to != settings.TEST_BLOCK_NOTIFY_RECIPIENTS[0],
                ])
            ])

            if should_send:
                print(f'Time to send a notification to {verify.code}')
                verify.email = email
                sent_to = verify.send_verify_request(
                    request,
                    date=mtg.date,
                    message=message,
                    force_to=settings.TEST_BLOCK_NOTIFY_RECIPIENTS
                )
                verify.sent_on = timezone.now()
                verify.sent_to = sent_to
                verify.confirmation_type = 'A'
                verify.save()

        self.send_schedule_update(request, date, message=message)

        return Response({"status": "success"})


class ScheduleVerifyView(APIView):
    permission_classes = ()

    def get(self, request, code=None, confirmation=None):
        """
        Player clicked a verification link
        """

        try:
            verify = ScheduleVerify.objects.get(code=code)
        except ScheduleVerify.DoesNotExist:
            pass
            # ToDo: Redirect to this link is no longer valid page!
        else:
            # Valid link
            if confirmation == 'confirm':
                verify.received_on = timezone.now()
                verify.confirmation_type = "C"
                verify.save()
                player_confirmed.send(verify,
                                      player=verify.schedule.player,
                                      request=request)
                return redirect(
                    reverse('schedule:response_confirmed'))
            elif confirmation == 'reject':
                verify.confirmation_type = "R"
                verify.received_on = timezone.now()
                verify.save()
                player_rejected.send(verify,
                                     player=verify.schedule.player,
                                     request=request)
                return redirect(
                    reverse('schedule:response_rejected'))
            else:
                # Invalid confirmation type
                # ToDo: Refer to error page
                pass

        # ToDo: Redirect to a confirmation page.
        response = redirect('/')
        return response


class BlockNotifyer(View):

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

    def build_notify_message(self, date, players):
        """
        Generate plain text version of message.
        """
        playerlist = self.build_player_list(players)

        prefix = "      - "
        couples = [f"{c[0]} and {c[1]}" for c in playerlist ]
        player_string = prefix + prefix.join(couples)

        msg = dedent(f"""
            =
            
            Here is the schedule for Friday, {date}:
            {player_string}
                        
        """)

        return msg

    def build_html_notify_message(self, date, players):
        """
        Generate an HTML Formatted version of the message.
        """

        playerlist = self.build_player_list(players)

        items = [
            f"<li><span>{c[0]}</span> and <span>{c[1]}</span></li>"
            for c in playerlist
        ]
        items_string = '\n'.join(items)

        msg = dedent(f"""
            <html>
            <head></head>
            <body>
                <h3>Here is the schedule 
                    for {date.strftime('%A, %B %-d')}:</h3>
    
            <ul>
                {items_string}
            </ul>
        """)

        return msg

    def post(self, request, date):
        tb = Scheduler()

        players = tb.query_schedule(date)

        from_email = settings.EMAIL_HOST_USER

        # Generate Text and HTML versions.
        message = self.build_notify_message(date, players)
        html = self.build_html_notify_message(date, players)

        subject = settings.BLOCK_NOTIFY_SUBJECT % date

        if settings.TEST_BLOCK_NOTIFY_RECIPIENTS:
            recipients = settings.TEST_BLOCK_NOTIFY_RECIPIENTS
            cc_list = []
        else:
            recipients, cc_list = tb.get_notify_email_lists()

        msg = EmailMultiAlternatives(subject=subject,
                                     body=message,
                                     from_email=from_email,
                                     to=recipients,
                                     cc=cc_list)
        msg.attach_alternative(html, 'text/html')

        msg.send()

        return JSONResponse({})
