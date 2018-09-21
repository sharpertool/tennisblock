from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Print the value of the components version'

    def add_arguments(self, parser):
        parser.add_argument('season', help='''
        Season to manipulate
        ''')

    def handle(self, *args, **options):

        pass