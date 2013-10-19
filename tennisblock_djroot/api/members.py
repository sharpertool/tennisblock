# Create your views here.


from django.views.generic.edit import View

from blockdb.models import Player,SeasonPlayers

from api.apiutils import JSONResponse,JSONParser, _currentSeason

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

            players = SeasonPlayers.objects.filter(season = currseason).order_by('player__last','player__first')

            for sp in players:

                p = self.serializeSeasonPlayer(sp)


                pdata.append(p)

            return JSONResponse(pdata)

    def post(self,request,*args, **kwargs):

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

