# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from TBLib.manager import TeamManager


class Command(BaseCommand):
    help = 'Pick Teams for the given date'

    def add_arguments(self, parser):
        parser.add_argument('date')
        parser.add_argument('--nodupes', action='store_true')
        parser.add_argument('--sequences', type=int, default=3)
        parser.add_argument('--test', '-t', action='store_true')
        parser.add_argument('--iterations', '-i', type=int, default=20)
        parser.add_argument('--tries', '-i', type=int, default=5)

    def handle(self, *args, **options):
        mgr = TeamManager()
        mgr.pick_teams_for_date(date=options['date'],
                                iterations=options['iterations'],
                                max_tries=options['tries'])
