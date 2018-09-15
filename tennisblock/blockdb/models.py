from django.db import models
from django.urls import reverse

from django.conf import settings

User = settings.AUTH_USER_MODEL


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
    lastdate = models.DateField(null=True)
    blocktime = models.TimeField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('season_detail', kwargs={'pk': self.pk})


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
    first = models.CharField(max_length=40)
    last = models.CharField(max_length=60)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    ntrp = models.FloatField()
    microntrp = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=14, blank=True)
    email = models.CharField(max_length=50, blank=True)

    objects = models.Manager()
    girls = GirlsManager()
    guys = GuysManager()
    season = models.ManyToManyField(Season, related_name='season_player')

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
        seasons = [s.season for s in self.seasonplayer_set.all()]
        return season in seasons


class BlockManager(models.Manager):
    use_for_related_fields = True

    def seasonPlayers(self):
        return self.filter()


class SeasonPlayer(models.Model):
    """
    Entry for each player for each season. Indicates that a given
    player is a member of the specified season.
    TODO: Expand to have unique values for a block, i.e. support more
    than just one block!


    """
    season = models.ForeignKey(Season, related_name='players', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    blockmember = models.BooleanField(default=False)

    objects = BlockManager()

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


class Meeting(models.Model):
    """
    Entry for each meeting night during the block season.
    There are entries for all nights, even holdouts. The holdout
    boolean indicates that this night is a holdout.

    Comments are not used, bug could indicate special information, i.e.
    special party night, etc.
    """
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    date = models.DateField()
    holdout = models.BooleanField(default=False)
    comments = models.CharField(max_length=128)

    def __str__(self):
        return "{}->{} holdout:{}".format(
                self.season, self.date, self.holdout
        )


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

    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='scheduled', on_delete=models.CASCADE)
    issub = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    partner = models.ForeignKey(Player, related_name='scheduled_partner', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} sub:{} verified:{}".format(
                self.meeting, self.player.name,
                self.issub, self.verified
        )


class Matchup(models.Model):
    """
    The matchup for a given meeting, set and court.
    Organizes players into two teams, t1 and t2, and a set of players
    each.
    """
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    set = models.IntegerField()
    court = models.IntegerField()
    team1_p1 = models.ForeignKey(Player, related_name="t1_p1", null=True, on_delete=models.CASCADE)
    team1_p2 = models.ForeignKey(Player, related_name="t1_p2", null=True, on_delete=models.CASCADE)
    team2_p1 = models.ForeignKey(Player, related_name="t2_p1", null=True, on_delete=models.CASCADE)
    team2_p2 = models.ForeignKey(Player, related_name="t2_p2", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{}:{} set:{} court:{} {}+{} vs {}+{}".format(
                self.meeting.season, self.meeting.date,
                self.set, self.court,
                self.team1_p1.name, self.team1_p2.name,
                self.team2_p1.name, self.team1_p2.name
        )
