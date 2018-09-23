# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from TBLib.teams import TeamManager

class Command(BaseCommand):
    help = 'Pick Teams for the given date'

    def add_arguments(self, parser):
        parser.add_argument('date')
        parser.add_argument('--nodupes', action='store_true')
        parser.add_argument('--sequences', type=int, default=3)
        parser.add_argument('--test', '-t', action='store_true')

    def handle(self, *args, **options):

        mgr = TeamManager()
        mgr.pickTeams(options['date'],
                      testing=options['test'],
                      n_sequences=options['sequences'],
                      noDupes=options['nodupes'])
