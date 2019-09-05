import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from django.conf import settings

User = settings.AUTH_USER_MODEL

VERIFY_CHOICES = (
    ('C', 'Confirm'),
    ('R', 'Reject'),
    ('A', 'Awaiting Response'),
)

CONFIRM_CHOICES = (
    ('A', 'Awaiting Response'),
    ('C', 'Schedule Confirmed'),
    ('R', 'Scheduled but not available'),
    ('U', 'Unconfirmed'),
)


class GirlsManager(models.Manager):
    def get_queryset(self):
        return super(GirlsManager, self).get_queryset().filter(gender='F')


class GuysManager(models.Manager):
    def get_queryset(self):
        return super(GuysManager, self).get_queryset().filter(gender='M')


class Player(models.Model):
    """
    Player object.

    This will be deprecated, as I add the player associated with the User account.
    """
    GENDER_CHOICES = (
        ('F', 'Gal'),
        ('M', 'Guy')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    # first = models.CharField(max_length=40)
    # last = models.CharField(max_length=60)
    # email = models.CharField(max_length=50, blank=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    ntrp = models.FloatField()
    microntrp = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=14, blank=True)

    objects = models.Manager()
    girls = GirlsManager()
    guys = GuysManager()

    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    get_full_name.short_description = 'Full name of player'
    full_name = property(get_full_name)

    @property
    def first(self):
        return self.user.first_name

    @property
    def last(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        if self.microntrp:
            un = self.microntrp
        else:
            un = self.ntrp
        return "{} {} {:3.1f},{:4.2f}".format(
            self.first, self.last, self.ntrp, un)

    def Name(self):
        return self.first + " " + self.last

    @property
    def name(self):
        return self.first + " " + self.last

    def in_season(self, season):
        """
        Return true if this player is a player in the given season.
        """
        try:
            if self.seasons.get(season):
                return True
        except ObjectDoesNotExist:
            return False


class Season(models.Model):
    """
    Define a block season.
    Gives a name, court information, and information about
    the start/end dates and block start date and time.
    """
    name = models.CharField(max_length=20)
    courts = models.IntegerField()
    firstcourt = models.IntegerField()
    startdate = models.DateField()
    enddate = models.DateField()
    blockstart = models.DateField()
    lastdate = models.DateField(blank=True, null=True)
    blocktime = models.TimeField()

    players = models.ManyToManyField(
        Player,
        related_name='seasons',
        through='SeasonPlayer'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('season:season_detail', kwargs={'pk': self.pk})


class SeasonPlayer(models.Model):
    """
    Entry for each player for each season. Indicates that a given
    player is a member of the specified season.
    TODO: Expand to have unique values for a block, i.e. support more
    than just one block!


    """
    season = models.ForeignKey(Season,
                               on_delete=models.CASCADE)
    player = models.ForeignKey(Player,
                               on_delete=models.CASCADE)
    blockmember = models.BooleanField(default=False)

    def __str__(self):
        return self.player.__str__()


def limit_to_gals():
    return {'gender': 'F'}


def limit_to_guys():
    return {'gender': 'M'}


class Couple(models.Model):
    """
    Link together players into couples. The couples are scheduled together.
    Individual players can be added as a substitute for a given night.

    Fulltime is a boolean. If False, then the couple will be considered as
    halftime. There are no options for 1/3 time, etc.

    I don't remember what canschedule is for....

    blockcouple: True if this couple is a member of the block. False for
    substitute couples.

    """

    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    male = models.ForeignKey(Player,
                             related_name='couple_guy',
                             limit_choices_to=limit_to_guys, on_delete=models.CASCADE)
    female = models.ForeignKey(Player,
                               related_name='couple_gal',
                               limit_choices_to=limit_to_gals, on_delete=models.CASCADE)
    fulltime = models.BooleanField(default=False)
    as_singles = models.BooleanField(default=False)
    canschedule = models.BooleanField(default=False)
    blockcouple = models.BooleanField(default=False)

    def __str__(self):
        return "{} {} and {} as {}".format(
            self.season, self.female.name, self.male.name,
            self.name
        )

    class Meta:
        unique_together = ('season', 'male', 'female',)


class Meeting(models.Model):
    """
    Entry for each meeting night during the block season.
    There are entries for all nights, even holdouts. The holdout
    boolean indicates that this night is a holdout.

    Comments are not used, bug could indicate special information, i.e.
    special party night, etc.
    """
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    meeting_index = models.IntegerField(default=0)
    date = models.DateField()
    holdout = models.BooleanField(default=False)
    comments = models.CharField(max_length=128)
    court_count = models.IntegerField(null=True)

    def __str__(self):
        return "{}->{} holdout:{}".format(
            self.season, self.date, self.holdout
        )

    @property
    def num_courts(self):
        if self.court_count is not None:
            return self.court_count
        return self.season.courts


class Availability(models.Model):
    """
    Entry for each player and each night. Boolean indicates that the
    player is available.
    """
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='available', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def __str__(self):
        return "availability for {} on {} is {}".format(
            self.player.name, self.meeting.date, self.available
        )


class AvailabilityManager(models.Manager):
    def get_for_season_player(self, player, season):
        try:
            av = PlayerAvailability.objects.get(player=player, season=season)
        except PlayerAvailability.DoesNotExist:
            mtgs = season.meeting_set.all()
            av = PlayerAvailability(player=player,
                                     season=season,
                                     available=[True for v in mtgs],
                                     scheduled=[False for v in mtgs],
                                     played=[False for v in mtgs])
            av.save()
        return av


class PlayerAvailability(models.Model):
    """
    Better optimized version of the original
    """
    player = models.ForeignKey(Player, related_name='availabiliy', on_delete=models.CASCADE)
    season = models.ForeignKey(Season,
                               on_delete=models.CASCADE)
    available = ArrayField(models.BooleanField(), blank=True, default=list)
    scheduled = ArrayField(models.BooleanField(), blank=True, default=list)
    played = ArrayField(models.BooleanField(), blank=True, default=list)

    objects = AvailabilityManager()

    def __str__(self):
        return "availability for {} on {} is {}".format(
            self.player.name, self.season, self.available
        )

    def save(self, **kwargs):
        if self.available == list():
            print('Initialize values on save if defaulted')
            mtgs = self.season.meeting_set.all()
            if mtgs.count():
                self.available = [True for v in range(mtgs.count())]
                self.scheduled = [False for v in range(mtgs.count())]
                self.played = [False for v in range(mtgs.count())]

        return super().save(**kwargs)


class Schedule(models.Model):
    """
    Each entry schedules a player to play on the given meeting.
    The player may be a sub.

    Verified is a boolean to indicate that the player has confirmed via
    text, phone, email, etc.

    NOT USED:The partner is the players partner for the night

    """
    class Meta:
        permissions = (
            ("change_sched", "Can change the schedule"),
        )

    meeting = models.ForeignKey(Meeting,
                                on_delete=models.CASCADE)
    player = models.ForeignKey(Player,
                               related_name='scheduled', on_delete=models.CASCADE)
    issub = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    confirmation_status = models.CharField(max_length=2, choices=CONFIRM_CHOICES,
                                           default='U')
    partner = models.ForeignKey(Player,
                                related_name='scheduled_partner',
                                null=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        partner_name = "---"
        if self.partner:
            partner_name = self.partner.name

        s1 = f"{self.meeting} {self.player.name} partner:{partner_name} "
        s2 = f"sub:{self.issub} verified:{self.verified}"
        return s1 + s2


class ScheduleVerify(models.Model):
    """
    Links used to verify a particular schedule item.
    These codes will be generated when a schedule is sent out.
    Users will be given the option to click "verify", or "reject"
    A reject link will mark them as scheduled, but not available.. that means
    someone needs to be scheduled in!
    Verified indicates they have confirmed their schedule
    """

    schedule = models.ForeignKey(Schedule,
                                 on_delete=models.CASCADE)
    code = models.UUIDField()
    created_on = models.DateTimeField(auto_created=True)
    confirmation_type = models.CharField(max_length=1, choices=VERIFY_CHOICES,
                                         default='A')

    @property
    def expired(self):
        return self.schedule.meeting.date > datetime.date.today()


class Matchup(models.Model):
    """
    The Matchup for a given meeting, set and court.
    Organizes players into two teams, t1 and t2, and a set of players
    each.
    """
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    set = models.IntegerField()
    court = models.IntegerField()
    team1_p1 = models.ForeignKey(Player,
                                 related_name="t1_p1",
                                 null=True,
                                 on_delete=models.CASCADE)
    team1_p2 = models.ForeignKey(Player,
                                 related_name="t1_p2",
                                 null=True,
                                 on_delete=models.CASCADE)
    team2_p1 = models.ForeignKey(Player,
                                 related_name="t2_p1",
                                 null=True,
                                 on_delete=models.CASCADE)
    team2_p2 = models.ForeignKey(Player,
                                 related_name="t2_p2",
                                 null=True,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return "{}:{} set:{} court:{} {}+{} vs {}+{}".format(
            self.meeting.season, self.meeting.date,
            self.set, self.court,
            self.team1_p1.name, self.team1_p2.name,
            self.team2_p1.name, self.team1_p2.name
        )
