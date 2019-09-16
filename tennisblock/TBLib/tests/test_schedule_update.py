from django.test import TestCase
from django.db import IntegrityError

from TBLib.season import SeasonManager

from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from TBLib.schedule import Scheduler

from api.blockschedule import ScheduleNotifyView

from blockdb.models import Schedule, ScheduleVerify

from blockdb.tests.db_utils import BlockDBTestBase

factory = APIRequestFactory()


class TestScheduleUpdate(BlockDBTestBase):

    @classmethod
    def setUpTestData(cls):
        results = cls.staticCoreSetup()
        [cls.guys, cls.girls, cls.season, cls.meetings] = results
        cls.splayers = cls.staticPlayersSetup(
            cls.season,
            cls.girls,
            cls.guys)
        cls.couples = cls.static_couples_setup(
            cls.season,
            cls.girls,
            cls.guys,
            fulltime=[1, 0, 0, 0, 0, 0, 0, 0],
            singles=[0, 0, 0, 0, 0, 1, 1, 1])

        cls.admin_user = cls.guys[0].user
        cls.admin_user.is_staff = True
        cls.admin_user.save()

        cls.season.courts = 2
        cls.season.save()

    def setUp(self):
        pass

    def couples_modify(self, fulltime=None, singles=None):
        for i, couple in enumerate(self.couples):
            couple.fulltime = fulltime[i]
            couple.as_singles = singles[i]
            couple.save()

    def build_couples(self):
        couples = []
        for couple in self.couples:
            couples.append({
                'guy': {
                    'id': couple.male.id,
                    'issub': False,
                    'verified': False
                },
                'gal': {
                    'id': couple.female.id,
                    'issub': False,
                    'verified': False
                }
            })
        return couples

    def test_initial_update(self):
        """
        Build structure of couples:
            couple: {'guy':
                        {'id': Player.pk, 'issub': Boolean, 'verified': Boolean},
                     'gal':
                        {'id': Player.pk, 'issub': Boolean, 'verified': Boolean},
                    }
            couples is array of couple
        :return:
        """
        meeting = self.meetings[0]
        couples = self.build_couples()
        scheduler = Scheduler()
        date = meeting.date.strftime("%Y-%m-%d")
        scheduler.update_schedule(date, couples)

        sch = Schedule.objects.filter(meeting=meeting).all()
        self.assertEqual(len(sch), len(couples)*2)
        self.assertEqual(ScheduleVerify.objects.all().count(), 0)

        for s in sch:
            v = s.get_verification()

        self.assertEqual(ScheduleVerify.objects.all().count(), len(couples)*2)

        self.assertEqual(
            ScheduleVerify.objects.filter(sent_on__isnull=True).count(), len(couples)*2)

        request = factory.post(reverse('api:scheduleverify_for_date', kwargs={'date': date}))
        force_authenticate(request, user=self.admin_user)
        response = ScheduleNotifyView.as_view()(request, date=date)
        self.assertEqual(response.status_code, 200)


    def test_udpate_single_player(self):
        pass

    def test_update_a_couple(self):
        pass

    def test_upodate_a_lot_of_stuff(self):
        pass
