from django.core.management.base import BaseCommand
import logging
from textwrap import dedent

from TBLib.manager import TeamManager
from TBLib.schedule import Scheduler

from TBLib.loader import load_matches

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = dedent('''
    Add a new season to the database.
''')

    def add_arguments(self, parser):
        parser.add_argument('schedule_date')

    def handle(self, *args, **options):
        """
        Add a new season to the block system.
        """

        s = TestScheduler()
        s.schedule(options['schedule_date'])


class TestScheduler:

    def schedule(self, date):

        scheduler = Scheduler()
        logger.info("blockSchedule POST for date:%s" % date)
        group = scheduler.get_next_group(date)
        logger.info("Groups:")
        for g in group:
            logger.info("\tHe:%s She:%s" % (g.male.Name(), g.female.Name()))

        scheduler.add_group_to_schedule(date, group)

        mgr = TeamManager()
        mgr.dbTeams.delete_matchup(date)

        sched = scheduler.query_schedule(date)
