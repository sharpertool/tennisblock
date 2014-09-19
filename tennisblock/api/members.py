# Create your views here.


from django.views.generic.edit import View

from blockdb.models import Player, SeasonPlayers
from django.contrib.auth.models import User

from .apiutils import JSONResponse, get_current_season


class SeasonPlayersView(View):
    members_only = True

    def serializeSeasonPlayer(self, sp):

        player = sp.player

        p = {
            'id': player.id,
            'first': player.user.first_name,
            'last': player.user.last_name,
            'gender': player.gender,
            'ntrp': player.ntrp,
            'microntrp': player.microntrp,
            'email': player.user.email,
            'phone': player.phone,
            'blockmember': sp.blockmember
        }
        return p

    def get(self, request, *args, **kwargs):

        currseason = get_current_season()

        if kwargs.get('id'):
            print("Getting one player..")
            players = SeasonPlayers.objects.filter(season=currseason, player__id=kwargs.get('id'))
            if len(players):
                p = self.serializeSeasonPlayer(players[0])
                return JSONResponse(p)

            return JSONResponse({})

        else:
            pdata = []

            players = SeasonPlayers.objects.filter(season=currseason) \
                .order_by('player__last', 'player__gender', 'player__first')

            for sp in players:
                p = self.serializeSeasonPlayer(sp)

                pdata.append(p)

            return JSONResponse(pdata)

    def post(self, request, *args, **kwargs):

        currseason = get_current_season()
        data = JSONParser().parse(request)

        if kwargs.get('id'):
            print("Updating one player..")
            players = SeasonPlayers.objects.filter(season=currseason, player__id=kwargs.get('id'))
            if len(players):
                sp = players[0]
                for key, val in data.iteritems():
                    if key == 'blockmember':
                        print("Updating blockmember value to %s" % val)
                        sp.blockmember = val
                        sp.save()

            return JSONResponse({})
        else:

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

        return JSONResponse({})

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

                sp = SeasonPlayers.objects.create(
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
        data = JSONParser().parse(request)
        member = data.get('member')

        if member:
            print("Deleting member! %s %s" % (
                member.get('first'), member.get('last')))

            print("Deleting player id(%s)" % member.get('id'))
            SeasonPlayers.objects.filter(
                season=currseason, player__id=member.get('id')).delete()
            Player.objects.filter(id=member.get('id')).delete()

            print("Player deleted.")

            return JSONResponse({})
