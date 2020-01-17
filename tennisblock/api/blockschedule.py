import random
import datetime
from textwrap import dedent
from django.views.generic.base import View
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.urls import reverse
from django.template import loader
from django.shortcuts import redirect
from django.db.models import Q, ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework import authentication, permissions
from blockdb.models import (Schedule, Couple, Player,
                            SeasonPlayer, Meeting, Availability,
                            PlayerAvailability,
                            ScheduleVerify)

from .apiutils import JSONResponse, get_current_season, get_meeting_for_date, time_to_js
from TBLib.manager import TeamManager
from TBLib.schedule import Scheduler


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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email']


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Player
        fields = ['pk', 'user', 'gender',
                  'ntrp', 'microntrp',
                  'phone'
                  ]


class AllPlayers(ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
