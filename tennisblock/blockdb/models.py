from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

class BlockManager(models.Manager):
    use_for_related_fields=True

    def seasonPlayers(self,**kwargs):
        return self.filter()

@python_2_unicode_compatible
class Season(models.Model):
     name               = models.CharField(max_length=20)
     courts             = models.IntegerField()
     firstcourt         = models.IntegerField()
     startdate          = models.DateField()
     enddate            = models.DateField()
     blockstart         = models.DateField()
     blocktime          = models.TimeField()

     def __str__(self):
         return self.name

class GirlsManager(models.Manager):
    def get_queryset(self):
        return super(GirlsManager, self).get_queryset().filter(gender='F')

class GuysManager(models.Manager):
    def get_queryset(self):
        return super(GuysManager, self).get_queryset().filter(gender='M')

@python_2_unicode_compatible
class Player(models.Model):
    GENDER_CHOICES= (
        ('F', 'Gal'),
        ('M', 'Guy')
    )

    first               = models.CharField(max_length=40)
    last                = models.CharField(max_length=60)
    gender              = models.CharField(max_length=1,choices= GENDER_CHOICES)
    ntrp                = models.FloatField()
    microntrp           = models.FloatField(null=True,blank=True)
    email               = models.CharField(max_length=50,blank=True)
    phone               = models.CharField(max_length=14,blank=True)

    objects = models.Manager()
    girls = GirlsManager()
    guys = GuysManager()

    def __str__(self):
        if self.microntrp:
            un = self.microntrp
        else:
            un = self.ntrp
        return "{} {} {:3.1f},{:4.2f}".format(self.first,self.last,self.ntrp,un)

    def Name(self):
        return self.first + " " + self.last

@python_2_unicode_compatible
class SeasonPlayers(models.Model):
    season              = models.ForeignKey(Season)
    player              = models.ForeignKey(Player)
    blockmember         = models.BooleanField(default=False)

    objects = BlockManager()

    def __str__(self):
        return self.player.__str__()

@python_2_unicode_compatible
class Couple(models.Model):
    season              = models.ForeignKey(Season)
    name                = models.CharField(max_length=50)
    male                = models.ForeignKey(Player,related_name='guy')
    female              = models.ForeignKey(Player,related_name='gal')
    fulltime            = models.BooleanField(default=False)
    canschedule         = models.BooleanField(default=False)
    blockcouple         = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Meetings(models.Model):
    season              = models.ForeignKey(Season)
    date                = models.DateField()
    holdout             = models.BooleanField(default=False)
    comments            = models.CharField(max_length=128)

class Availability(models.Model):
    meeting             = models.ForeignKey(Meetings)
    player              = models.ForeignKey(Player)
    available           = models.BooleanField(default=True)

class Schedule(models.Model):

    class Meta:
        permissions = (
            ("change_sched", "Can change the schedule"),
        )

    meeting             = models.ForeignKey(Meetings)
    player              = models.ForeignKey(Player)
    issub               = models.BooleanField(default=False)
    verified            = models.BooleanField(default=False)
    partner             = models.ForeignKey(Player,related_name='partner',null=True)

class Matchup(models.Model):
    meeting             = models.ForeignKey(Meetings)
    set                 = models.IntegerField()
    court               = models.IntegerField()
    team1_p1            = models.ForeignKey(Player,related_name="t1_p1",null=True)
    team1_p2            = models.ForeignKey(Player,related_name="t1_p2",null=True)
    team2_p1            = models.ForeignKey(Player,related_name="t2_p1",null=True)
    team2_p2            = models.ForeignKey(Player,related_name="t2_p2",null=True)


