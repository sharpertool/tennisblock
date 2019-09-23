# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from TBLib.schedule import reset_availability_arrays


class Command(BaseCommand):
    help = 'Reset availability arrays for current season'

    def add_arguments(self, parser):
        parser.add_argument('--date')

    def handle(self, *args, **options):
        reset_availability_arrays(date=options['date'])
