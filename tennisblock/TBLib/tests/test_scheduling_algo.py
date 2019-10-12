"""
Test the Scheduling Algorithm

Here are the goals:
    - Schedule a full set of players from the current set of block players
    - Do not schedule players that are not available
    - Prioritize players with the least amount of plays
    - Schedule couples together
    - Schedule single players in the schedule with equal priority as copules
    - Boost priority of players that are not available for the next schedule
    - 2X Boost priority of players that are not available for next 2 schedules
    - Maximum boost for any players that are available this week, and not next 3+ weeks


"""
from django.test import tag
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from blockdb.models import (
    Season, Meeting, SeasonPlayer,
    PlayerAvailability, Player
)

from blockdb.tests.db_utils import BlockDBTestBase
from api.notify import ScheduleNotifyView
from TBLib.schedule import Scheduler


factory = APIRequestFactory()


def notify_post(msg, user=None):
    request = factory.post(reverse('api:notify', kwargs={'date': '0000-00-00'}),
                           {"message": msg})
    if user:
        force_authenticate(request, user=user)
    response = ScheduleNotifyView.as_view()(request)
    return response


@tag('medium')
class TestBlockSchedule(BlockDBTestBase):

    @classmethod
    def setUpTestData(cls):
        guys, girls, season, meetings = cls.staticCoreSetup(num_players=16)
        players = cls.staticPlayersSetup(season, girls, guys)
        guys[0].user.is_staff = True
        guys[0].user.save()

        cls.static_meeting_setup(meetings, girls, guys)
        cls.admin_user = guys[0].user
        cls.guys = guys
        cls.girls =girls
        cls.season = season
        cls.meeting = meetings
        cls.splayers = players

    def setUp(self):
        pass

    def test_get_available_couples(self):
        pass

