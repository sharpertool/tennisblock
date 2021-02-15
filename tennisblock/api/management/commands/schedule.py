# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from TBLib.schedule import Scheduler
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Pick Match for the given date'

    def add_arguments(self, parser):
        parser.add_argument('date')

    def handle(self, *args, **options):
        date = options['date']
        logger.info("blockSchedule POST for date:%s" % date)

        sched = Scheduler.generate_schedule(date)

        if sched is None:
            logger.error(f"Invalid date specified, no meetings on that date.")
        else:
            logger.info(f"Schedule for date is {sched}")
