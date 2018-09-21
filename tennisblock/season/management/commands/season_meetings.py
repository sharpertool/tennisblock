from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Print the value of the components version'

    def add_arguments(self, parser):
        parser.add_argument('season', help='''
        Season to manipulate
        ''')

    def handle(self, *args, **options):

        with open(options.get('tmpfile'), 'w') as fp:
            fp.write(f"{settings.COMPONENTS_VERSION}")




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
