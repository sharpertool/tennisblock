# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from TBLib.schedule import update_availability_played_arrays


class Command(BaseCommand):
    help = 'Update the played array in availability'

    def handle(self, *args, **options):
        update_availability_played_arrays()
