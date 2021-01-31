# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic.edit import View
from django.db.models import Q

from blockdb.models import Player, SeasonPlayer
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .apiutils import JSONResponse, get_current_season


class SeasonPossibleSubs(APIView):
    """ List of Players That can be added to season as subs """


class SeasonSubs(APIView):
    """ List of Players That can be added to season as subs """

    def get(self, request, *args, **kwargs):
        season = get_current_season()

        season_players = SeasonPlayer.objects.filter(season=season)
        sp_ids = season_players.filter(blockmember=True).values_list('player__pk', flat=True)
        subs_ids = season_players.filter(blockmember=False).values_list('player__pk', flat=True)

        moresubs = Player.objects.filter(
            ~Q(pk__in=sp_ids) & ~Q(pk__in=subs_ids)
        ).values_list('pk', flat=True)
        return Response({
            'status': 'success',
            'subs': subs_ids,
            'moresubs': moresubs
        })

    def put(self, request):
        id = request.data.get('id')
        print(f"Toggle this id: {id}")
        player = get_object_or_404(Player, pk=id)
        season = get_current_season()

        created = False
        try:
            sp = SeasonPlayer.objects.get(
                season=season,
                player=player
            )
            sp.delete()
        except SeasonPlayer.DoesNotExist:
            sp = SeasonPlayer.objects.create(
                season=season,
                player=player,
                blockmember=False)
            created = True

        return Response({
            'status': 'success',
            'created': created
        })


class SeasonPlayerView(APIView):
    members_only = True

    def serializeSeasonPlayer(self, sp):

        player = sp.player

        p = {
            'id': player.id,
            'first': player.first,
            'last': player.last,
            'gender': player.gender,
            'ntrp': player.ntrp,
            'microntrp': player.microntrp,
            'email': player.email,
            'phone': player.phone,
            'blockmember': sp.blockmember,
            'fulltime': sp.fulltime,
        }
        return p

    def get(self, request, *args, **kwargs):

        currseason = get_current_season()

        if kwargs.get('id'):
            print("Getting one player..")
            players = SeasonPlayer.objects.filter(
                season=currseason, player__id=kwargs.get('id'))
            if len(players):
                p = self.serializeSeasonPlayer(players[0])
                return JSONResponse(p)

            return JSONResponse({})

        else:
            pdata = []

            players = SeasonPlayer.objects.filter(season=currseason)
            players = players.order_by(
                'player__user__last_name',
                'player__gender'
            )

            for sp in players:
                p = self.serializeSeasonPlayer(sp)
                pdata.append(p)

            return JSONResponse(pdata)

    def post(self, request, *args, **kwargs):

        currseason = get_current_season()

        if kwargs.get('id'):
            print(f"Updating one player.. {kwargs.get('id')}")
            players = SeasonPlayer.objects.all()
            players = players.filter(season=currseason,
                                     pk=kwargs.get('id'))
            if len(players):
                sp = players[0]
                if 'blockmember' in request.data:
                    val = False
                    if request.data['blockmember'] == 'true':
                        val = True
                    print(f"Updating blockmember value to {val}")
                    print(f"Season Player {sp} id:{sp.pk}")
                    sp.blockmember = val
                    sp.save()

            return Response({'status': 'success'})
        else:

            member = request.data.get('member')

            fields = [
                'first',
                'last',
                'gender',
                'ntrp',
                'microntrp',
                'email',
                'phone'
            ]

            if member:
                print("I got a member! id(%s) %s %s" % (
                    member.get('id'),
                    member.get('first'), member.get('last')))

                try:
                    player = Player.objects.get(pk=int(member.get('id', -1)))
                    print("Found the player object.")
                    orig = member.get('original')
                    for fld in fields:
                        if member.get(fld) != orig.get(fld):
                            setattr(player, fld, member.get(fld))

                    player.save()

                except Exception as e:
                    print("Error updating the player player!:%s" % e)

        return Response({'status': 'success'})

    def put(self, request, *args, **kwargs):
        """
        Used to insert a new member
        """
        currseason = get_current_season()
        data = JSONParser().parse(request)
        member = data.get('member')

        fields = [
            'first',
            'last',
            'gender',
            'ntrp',
            'microntrp',
            'email',
            'phone'
        ]

        if member:
            print("I got a new member! %s %s" % (
                member.get('first'), member.get('last')))

            try:
                username = "{}.{}".format(member.get('first').lower(),
                                          member.get('last').lower())

                user = User.objects.create_user(username,
                                                member.get('email'))
                user.save()

                player = Player.objects.create(
                    user=user,
                    first=member.get('first'),
                    last=member.get('last'),
                    gender=member.get('gender'),
                    ntrp=member.get('ntrp'),
                    microntrp=member.get('microntrp'),
                    email=member.get('email'),
                    phone=member.get('phone'),
                )
                player.save()

                sp = SeasonPlayer.objects.create(
                    season=currseason,
                    player=player,
                    blockmember=member.get('blockmember', False)
                )
                sp.save()

                p = self.serializeSeasonPlayer(sp)

                return JSONResponse(p)

            except Exception as e:
                print("Error inserting the player player!:%s" % e)

        return JSONResponse({})

    def delete(self, request, *args, **kwargs):
        """
        Remove a member by ID
        """

        currseason = get_current_season()
        id = request.data.get('id')

        if id:
            print(f"Deleting member! {id}")
            try:
                p = SeasonPlayer.objects.get(season=currseason, pk=id)
                p.delete()
                return Response({'status': 'success'})
            except SeasonPlayer.DoesNotExist:
                return Response({'status': 'fail', 'error': 'Does not exist'})
        else:
            return Response({'status': 'fail', 'error': 'Missing id'})
