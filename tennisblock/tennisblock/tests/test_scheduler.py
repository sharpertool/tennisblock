"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from TBLib.schedule import Scheduler
from api.apiutils import get_current_season,get_next_meeting,get_meeting_for_date


# class SchedulerTest(TestCase):
#     fixtures=['auth_user','blockdb_test']
#
#     def setUp(self):
#         pass
#
#     def test_couples_weight(self):
#         """
#         Test the weighting algorithm for the couples
#         """
#         s = Scheduler()
#         season = get_current_season()
#
#         g = s.getNextGroup()


