

from django.db import connection
from excel import Excel

from blockdb.models import Player,Couple,Season,SeasonPlayers


class PlayerExcel(Excel):

    def __init__(self):
        pass


    def importExcel(self,xlfile):
        """
        Import the excel file that contains the players.

        """

        print("Importing Excel file %s" % xlfile)

        wb = self.openWorkbook(xlfile)

        ws = self.getSheet(wb,'Players')
        if ws == None:
            print("Players worksheet not found in %s" % xlfile)
            return

        nrows = self.getRowCount(ws)
        rowHeadings = self.getValues(ws,0)

        self.colParams = []

        print ("Getting Players")
        players = []
        for rowid in range(1,nrows):
            theRow = self.getValues(ws,rowid)
            player = dict(zip(rowHeadings, theRow))
            if not player['First'] == "" and not player['Last'] == "":
                players.append(player)

        return players


def currentSeason():

    return Season.objects.get(name="Fall 2013")


def addPlayer(player):
    lname = player['Last']
    fname = player['First']

    try:
        p = Player.objects.get(last=lname,first=fname)

        # If player exist, update, otherwise, add
        p.ntrp = player['NTRP']
        p.microntrp = player['uNTRP']
        if player['email'] != '':
            p.email = player['email']
        if player['home'] != '':
            p.phone = player['home']
        p.save()

    except:
        p = Player.objects.create(
            first       = fname,
            last        = lname,
            gender      = player['Gender'].upper(),
            ntrp        = player['NTRP'],
            microntrp   = player['uNTRP']
        )
        if player['email'] != '':
            p.email = player['email']
        if player['home'] != '':
            p.phone = player['home']

        p.save()

    return p


def addPlayers(players):
    """
    Add or update players.

    If the player first+last name exists, then update values, otherwise, add a new player.
    """

    for player in players:
        addPlayer(player)


def addSeasonPlayers(season,players):
    """
    Add players to the season players table.

    """

    #SeasonPlayers.objects.filter(season=season).delete()
    for player in players:
        lname = player['Last']
        fname = player['First']

        try:
            p = Player.objects.get(last=lname,first=fname)
        except:
            p = addPlayer(player)

        try:
            sp = SeasonPlayers.objects.get(
                season=season,
                player=p)

            sp.blockmember = True
            sp.save()
        except:
            sp = SeasonPlayers.objects.create(
                season      =season,
                player      = hasp,
                blockmember = True
            )
            sp.save()

def addCouples(season,players):
    #Couple.objects.filter(season=season).delete()

    couples = {}

    for player in players:
        cname = player['Couplename']

        if cname != "":
            if not couples.has_key(cname):
                couples[cname] = {}
            couples[cname][player['Gender']] = player

    print("Updated the couples")

    for couple in couples:
        cdata = couples[couple]

        theguy = cdata['m']
        thegal = cdata['f']

        guy = Player.objects.get(
            last=theguy['Last'],
            first=theguy['First'])
        gal = Player.objects.get(
            last=thegal['Last'],
            first=thegal['First'])

        try:
            c = Couple.objects.get(
                season=season,
                name=couple
            )

            c.fulltime = theguy['FullTime']
            c.canschedule = theguy['blockmember']
            c.blockcouple = theguy['blockmember']

            c.male = guy
            c.female = gal
            c.save()

        except:
            c = Couple.objects.create(
                season      = season,
                name        = couple,
                male        = guy,
                female      = gal,
                fulltime    = theguy['FullTime'],
                canschedule = theguy['blockmember'],
                blockcouple = theguy['blockmember']
            )
            c.save()
