from django.core.management.base import BaseCommand
from os.path import exists

from optparse import make_option
from textwrap import dedent

from lib.season import BlockSeason,SeasonManager

class Command(BaseCommand):
    args = ''
    help = dedent('''
    Add a new season to the database.
''')

    option_list = BaseCommand.option_list + (
        make_option('--season',
                    dest='season',
                    help=''),
        make_option('--num_courts',
                    dest='num_courts',
                    type='int',
                    help=''),
        make_option('--first_court',
                    dest='first_court',
                    type='int',
                    help=''),
        make_option('--season_start',
                    dest='season_start',
                    help=''),
        make_option('--season_end',
                    dest='season_end',
                    help=''),
        make_option('--block_start',
                    dest='block_start',
                    help=''),
        make_option('--block_time',
                    dest='block_time',
                    help=''),
        make_option('--holdouts',
                    dest='holdouts',
                    help=''),
    )

    def handle(self, *args, **options):
        """
        Add a new season to the block system.
        """

        bs = BlockSeason(season=options.get('season'),
                         num_courts=options.get('num_courts'),
                         first_court=options.get('first_court'),
                         season_start=options.get('season_start'),
                         season_end=options.get('season_end'),
                         block_start=options.get('block_start'),
                         block_time=options.get('block_time'),
                         holdouts=options.get('holdouts')
        )

        mgr = SeasonManager()

        mgr.addSeason(bs)

        mgr.addAllCurrentPlayers(bs.season)
