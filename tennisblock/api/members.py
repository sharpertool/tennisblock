# Create your views here.


from django.views.generic.edit import View

from tennisblock.blockdb.models import Player,SeasonPlayers

from .apiutils import JSONResponse,JSONParser, _currentSeason

class SeasonPlayersView(View):
    members_only = True

    def serializeSeasonPlayer(self,sp):

        player = sp.player

        p = {
            'id'            : player.id,
            'first'         : player.first,
            'last'          : player.last,
            'gender'        : player.gender,
            'ntrp'          : player.ntrp,
            'microntrp'     : player.microntrp,
            'email'         : player.email,
            'phone'         : player.phone,
            'blockmember'   : sp.blockmember
        }
        return p


    def get(self,request,*args, **kwargs):

        currseason = _currentSeason()

        if kwargs.get('id'):
            print("Getting one player..")
            players = SeasonPlayers.objects.filter(season = currseason,player__id = kwargs.get('id'))
            if len(players):
                p = self.serializeSeasonPlayer(players[0])
                return JSONResponse(p)

            return JSONResponse({})

        else:
            pdata = []

            players = SeasonPlayers.objects.filter(season = currseason)\
                .order_by('player__last','player__gender','player__first')

            for sp in players:

                p = self.serializeSeasonPlayer(sp)


                pdata.append(p)

            return JSONResponse(pdata)

    def post(self,request,*args, **kwargs):

        currseason = _currentSeason()
        data = JSONParser().parse(request)

        if kwargs.get('id'):
            print("Updating one player..")
            players = SeasonPlayers.objects.filter(season = currseason,player__id = kwargs.get('id'))
            if len(players):
                sp = players[0]
                for key,val in data.iteritems():
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
                    member.get('first'),member.get('last')))

                try:
                    player = Player.objects.get(pk=int(member.get('id',-1)))
                    print("Found the player object.")
                    orig = member.get('original')
                    for fld in fields:
                        if member.get(fld) != orig.get(fld):
                            setattr(player,fld,member.get(fld))

                    player.save()

                except Exception as e:
                    print("Error updating the player player!:%s" % e)


        return JSONResponse({})

    def put(self,request,*args,**kwargs):
        """
        Used to insert a new member
        """
        currseason = _currentSeason()
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
                member.get('first'),member.get('last')))

            try:
                player = Player.objects.create(
                    first   = member.get('first'),
                    last    = member.get('last'),
                    gender  = member.get('gender'),
                    ntrp    = member.get('ntrp'),
                    microntrp = member.get('microntrp'),
                    email   = member.get('email'),
                    phone   = member.get('phone'),
                )
                player.save()

                sp = SeasonPlayers.objects.create(
                    season=currseason,
                    player=player,
                    blockmember = member.get('blockmember',False)
                )
                sp.save()

                p = self.serializeSeasonPlayer(sp)

                return JSONResponse(p)

            except Exception as e:
                print("Error inserting the player player!:%s" % e)


        return JSONResponse({})

    def delete(self,request,*args,**kwargs):
        """
        Remove a member by ID
        """

        currseason = _currentSeason()
        data = JSONParser().parse(request)
        member = data.get('member')

        if member:
            print("Deleting member! %s %s" % (
                member.get('first'),member.get('last')))

            print("Deleting player id(%s)" % member.get('id'))
            SeasonPlayers.objects.filter(season = currseason,player__id = member.get('id')).delete()
            Player.objects.filter(id=member.get('id')).delete()

            print("Player deleted.")

            return JSONResponse({})
