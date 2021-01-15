from django.core.management.base import BaseCommand
from os.path import exists

from optparse import make_option
from textwrap import dedent

from TBLib.loader import save_matches


class Command(BaseCommand):
    help = dedent('''
    Add a new season to the database.
''')

    def add_arguments(self, parser):
        parser.add_argument('--outfile')

    def handle(self, *args, **options):
        """
        Add a new season to the block system.
        """

        save_matches(options['outfile'])
