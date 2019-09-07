from django.test import tag

from blockdb.models import (
    Season, Meeting, SeasonPlayer,
    PlayerAvailability
)

from blockdb.tests.db_utils import BlockDBTestBase

@tag('medium')
class TestBlockSchedule(BlockDBTestBase):

    def setUp(self):
        self.coreSetup()
        self.playersSetup()

    def test_sub_list(self):
        pass

    def test_build_meetings(self):
        self.assertEqual(1, Season.objects.all().count(), "Should have had 16 meetings")
        self.assertEqual(16, Meeting.objects.all().count(), "Should have had 16 meetings")
        self.assertEqual(16, SeasonPlayer.objects.all().count())
        avlist = PlayerAvailability.objects.all()
        for av in avlist:
            self.assertEqual(len(av.available), 16, 'Expected availability to have 16 items')

    def test_block_players_get(self):
        pass

    def test_block_players_post(self):
        pass

    def test_block_dates_query(self):
        pass

    def test_block_schedule_query(self):
        pass

    def test_block_schedule_update(self):
        pass

    def test_block_schedule_delete(self):
        pass
