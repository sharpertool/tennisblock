from rest_framework.test import APIRequestFactory, force_authenticate
from django.test import tag
from django.urls import reverse
from unittest import mock

from blockdb.models import (
    Couple
)

from api.views.season import CouplesView
from blockdb.tests.db_utils import TennisTestSetup

request_factory = APIRequestFactory()


@tag('medium')
class TestBlockSchedule(TennisTestSetup):

    def setUp(self):
        self.coreSetup()
        self.playersSetup()

    def test_couples_query_requires_admin(self):
        self.user = self.guys[0].user

        request = request_factory.get(reverse('api:couples_for_season', kwargs={"season_id": 0}))
        force_authenticate(request, user=self.user)
        view = CouplesView.as_view()
        result = view(request, season_id=self.season.pk)

        self.assertEqual(result.status_code, 403, 'Expected to reject query if not an admin user')

    def test_couples_query(self):
        self.user = self.guys[0].user
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        gcs = mock.MagicMock(return_value=self.season)
        with mock.patch('api.views.season.gcs', gcs):
            request = request_factory.get(reverse('api:couples_for_season', kwargs={"season_id": 0}))
            force_authenticate(request, user=self.user)
            view = CouplesView.as_view()
            #result = view(request, season_id=self.season.pk)
            result = view(request)

        self.assertEqual(result.status_code, 200, 'Expected valid couples data')
        self.assertEqual(result.data.get('couples'), [])
        players = result.data.get('players')
        self.assertTrue('guys' in players)
        self.assertTrue('girls' in players)
        self.assertEqual(len(players.get('guys')), 8)
        self.assertEqual(len(players.get('girls')), 8)

    def test_couples_update(self):
        self.user = self.guys[0].user
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        data = {
            'couples': [
                {
                    'name': 'Hendersons',
                    'guy_id': self.guys[0].id,
                    'girl_id': self.girls[0].id,
                    'fulltime': True,
                    'as_singles': False,
                },
                {
                    'name': 'Hendersons',
                    'guy_id': self.guys[1].id,
                    'girl_id': self.girls[1].id,
                    'fulltime': False,
                    'as_singles': True,
                }

            ]
        }

        gcs = mock.MagicMock(return_value=self.season)
        with mock.patch('api.views.season.gcs', gcs):
            request = request_factory.post(reverse('api:couples_for_season', kwargs={"season_id": 0}), data, format='json')
            force_authenticate(request, user=self.user)
            view = CouplesView.as_view()
            result = view(request)

        self.assertEqual(result.status_code, 200, 'Expected valid couples data')
        self.assertEqual(result.data.get('status'), 'success')

        self.assertEqual(Couple.objects.filter(season=self.season).count(), 2)

