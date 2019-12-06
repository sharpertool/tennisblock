from django.contrib.gis.geos import GEOSGeometry

import factory
import factory.fuzzy
from faker import Factory
import datetime
import wagtail_factories
from . import models
from blockdb.models import (Player, Season, Meeting, SeasonPlayer,
                            Couple, PlayerAvailability, Schedule,
                            Matchup, ScheduleVerify)
from blockdb import signals
from django.db.models.signals import post_save
from django.contrib.auth.models import User

myGenerator = Factory.create('en_US')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')


class GirlUserFactory(UserFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name_female')
    last_name = factory.Faker('last_name_female')
    email = factory.Faker('email')


class GuyUserFactory(UserFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name_male')
    last_name = factory.Faker('last_name_male')
    email = factory.Faker('email')


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player

    user = factory.SubFactory(UserFactory)
    gender = 'F'
    ntrp = factory.fuzzy.FuzzyFloat(low=3.0, high=5.0)
    microntrp = factory.lazy_attribute(lambda o: o.ntrp)
    # phone = myGenerator.phone_number()
    phone = '208 861-5756'


class GuyPlayerFactory(PlayerFactory):
    class Meta:
        model = Player

    user = factory.SubFactory(GuyUserFactory)
    gender = 'M'


class GirlPlayerFactory(PlayerFactory):
    class Meta:
        model = Player

    user = factory.SubFactory(GirlUserFactory)
    gender = 'F'


class SeasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Season

    name = factory.Sequence(lambda n: f"season_{n}")
    courts = 4
    firstcourt = 9
    #startdate = factory.fuzzy.FuzzyDate(start_date=datetime.date(2019, 9, 1), end_date=datetime.date(2019, 9, 30))
    startdate = factory.LazyAttribute(lambda o: o.start_date)
    enddate = factory.LazyAttribute(lambda o: o.startdate + o.duration)
    lastdate = factory.LazyAttribute(lambda o: o.startdate + o.duration)
    blockstart = factory.LazyAttribute(lambda o: o.startdate + datetime.timedelta((4 - o.startdate.weekday()) % 7))
    blocktime = '19:00:00'

    class Params:
        start_date = datetime.date(2019, 9, 16)
        duration = datetime.timedelta(weeks=16) + datetime.timedelta(days=-1)


@factory.django.mute_signals(post_save)
class MutedSeasonFactory(SeasonFactory):
    pass


class MeetingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meeting

    season = factory.Iterator(models.Season.objects.all())
    season_index = 0
    date = factory.lazy_attribute(lambda o: o.season.blockstart + datetime.timedelta(weeks=o.season_index))
    holdout = False
    court_count = factory.lazy_attribute(lambda o: o.season.courts)


@factory.django.mute_signals(post_save)
class MutedMeetingFactory(MeetingFactory):
    pass


class SeasonPlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SeasonPlayer

    season = factory.Iterator(models.Season.objects.all())
    player = factory.Iterator(models.Player.objects.all())
    blockmember = True


class CoupleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Couple

    season = factory.Iterator(models.Season.objects.all())

    fulltime = True
    as_singles = False
    canschedule = True
    blockcouple = True


class PlayerAvailabilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlayerAvailability

    season = factory.Iterator(models.Season.objects.all())
    player = factory.Iterator(models.Player.objects.all())


class ScheduleFactory(factory.django.DjangoModelFactory):
    """
    Schedule a single player on a single meeting date
    There will be ncourts * 4 Schedule objects per meeting.
    """
    class Meta:
        model = Schedule

    meeting = None
    player = None
    partner = None

    issub = False
    verified = False
    confirmation_status = 'U'


class ScheduleVerifyFactory(factory.django.DjangoModelFactory):
    """
    Model used to keep track of schedule verify links
    """
    class Meta:
        model = ScheduleVerify

    schedule = None
    code = factory.Faker('uuid4')
    confirmation_type = 'A'


class MatchupFactory(factory.django.DjangoModelFactory):
    """
    The Matchup model keeps track of the calculated play matchups for the play date
    For each meeting, there will be ncourts * nsets Matchup objects.
    Each Matchup object describes a single game. There will be one per court,
    and multiple sets of Matchups for however many times the groups switches that date,
    usually 1, 2 or 3 times.
    """
    class Meta:
        model = Matchup

    meeting = None
    set = factory.Sequence(lambda n: n)
    court = factory.Sequence(lambda n: n)
    team1_p1 = None
    team1_p2 = None
    team2_p1 = None
    team2_p2 = None


