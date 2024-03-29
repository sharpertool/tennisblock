from django.test import tag
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from blockdb.models import (
    Season, Meeting, SeasonPlayer,
    PlayerAvailability, Player
)

from blockdb.tests.db_utils import BlockDBTestBase
from api.notify import ScheduleNotifyView
from api.blockschedule import BlockPlayers
from api.apiutils import get_meeting_for_date
from TBLib.schedule import Scheduler


factory = APIRequestFactory()


class TestBase(BlockDBTestBase):

    @classmethod
    def setUpTestData(cls):
        guys, girls, season, meetings = cls.staticCoreSetup()
        players = cls.staticPlayersSetup(season, girls, guys)
        guys[0].user.is_staff = True
        guys[0].user.save()

        cls.static_meeting_setup(meetings, girls, guys)
        cls.admin_user = guys[0].user
        cls.guys = guys
        cls.girls = girls
        cls.season = season
        cls.meeting = meetings
        cls.splayers = players

    @staticmethod
    def notify_post(msg, user=None):
        request = factory.post(reverse('api:notify', kwargs={'date': '0000-00-00'}),
                               {"message": msg})
        if user:
            force_authenticate(request, user=user)
        response = ScheduleNotifyView.as_view()(request, date='0000-00-00')
        return response


@tag('medium')
class TestBlockSchedule(TestBase):

    def setUp(self):
        pass

    def test_sub_list(self):
        pass

    def test_build_meetings(self):
        self.assertEqual(1, Season.objects.all().count(), "Should have had 16 meetings")
        self.assertEqual(16, Meeting.objects.all().count(), "Should have had 16 meetings")
        self.assertEqual(16, SeasonPlayer.objects.all().count())
        avlist = PlayerAvailability.objects.all()
        for av in avlist:
            self.assertEqual(len(av.available), 16, 'Expected availability to have 16 items')

    def test_schedule_notify(self):
        response = self.notify_post('This is a test message', user=self.admin_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': 'success'})

    def test_block_players_get(self):
        pass

    def test_block_players_post(self):
        pass

    def test_block_dates_query(self):
        pass

    def test_block_schedule_query(self):
        request = factory.get(reverse(
            'api:blockplayers_for_date', kwargs={'date': '0000-00-00'})
        )
        user = self.admin_user
        if user:
            force_authenticate(request, user=user)
        response = BlockPlayers.as_view()(request, date='2019-09-27')

        pass

    def test_block_schedule_update(self):
        date = '2019-09-27'
        mtg = get_meeting_for_date(date)
        couples = Scheduler.get_couples(mtg)

        result = Scheduler.update_schedule(date, couples)
        new_couples = Scheduler.get_couples(mtg)
        self.assertEqual(couples, new_couples)
        pass

    def test_block_schedule_delete(self):
        pass
