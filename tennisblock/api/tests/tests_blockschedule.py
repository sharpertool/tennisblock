import datetime

from django.test import TestCase, tag
from django.http import HttpRequest
from unittest import mock
from collections import namedtuple

from api.blockschedule import getSubList


@tag('medium')
class TestBlockSchedule(TestCase):

    def setUp(self):
        pass

    def test_sub_list(self):
        self.assertEqual(0, 1, 'Force a TDD failure')

    def test_build_meetings(self):
        result = getSubList(HttpRequest(), datetime.date(2019, 2, 1))
        self.assertEqual(0, 1, 'Force a failure for building meetings')

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
