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
                    help='The name of the season, i.e. Fall, 2014.'),
        make_option('--num_courts',
                    dest='num_courts',
                    type='int',
                    help='The number of courts.'),
        make_option('--first_court',
                    dest='first_court',
                    type='int',
                    help='The first court number. Must be one of 1,6 or 9.'),
        make_option('--season_start',
                    dest='season_start',
                    help='The date that the official block season starts.'),
        make_option('--season_end',
                    dest='season_end',
                    help='The date that the official block season ends.'),
        make_option('--block_start',
                    dest='block_start',
                    help=dedent('''
                    The date of the first block meeting.
                    This value sets the day of the week for the block, i.e.
                     if the block_start is a Thursday, then each thursday between
                     the season_start and season_end will be possible values.
                    ''')),
        make_option('--block_time',
                    dest='block_time',
                    help='The block time as a string value, i.e. 7PM.'),
        make_option('--holdouts',
                    dest='holdouts',
                    help='Specify the list of holdouts dates in a comma seperated list.'),
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
