from django.core.management.base import BaseCommand
from os.path import exists

from optparse import make_option
from textwrap import dedent

from lib.block import (
    PlayerExcel,
    currentSeason,
    addCouples,
    addPlayers,
    addSeasonPlayers
)

class Command(BaseCommand):
    args = ''
    help = dedent('''
    Add players for the new season
''')

    option_list = BaseCommand.option_list + (
        make_option('xlfile',
                    dest='xlfile',
                    help='XL File containing the player lists.'),
    )



    def handle(self, *args, **options):
        """
        Add Players.
        """

        xlfile = options.get('xlfile')

        if not exists(args.xlfile):
            raise Exception("Specified Excel file  %s does not exist." % xlfile)

        pe = PlayerExcel()
        players = pe.importExcel(xlfile)

        print("Imported %d players" % len(players))

        season = currentSeason()
        addPlayers(players)

        addSeasonPlayers(season,players)

        addCouples(season,players)
