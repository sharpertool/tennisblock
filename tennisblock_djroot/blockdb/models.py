from django.db import models

# Create your models here.

class BlockManager(models.Manager):
    use_for_related_fields=True

    def seasonPlayers(self,**kwargs):
        return self.filter()

class Season(models.Model):
     name               = models.CharField(max_length=20)
     courts             = models.IntegerField()
     firstcourt         = models.IntegerField()
     startdate          = models.DateField()
     enddate            = models.DateField()
     blockstart         = models.DateField()
     blocktime          = models.TimeField()

     def __unicode__(self):
         return self.name

class GirlsManager(models.Manager):
    def get_query_set(self):
        return super(GirlsManager, self).get_query_set().filter(gender='F')

class GuysManager(models.Manager):
    def get_query_set(self):
        return super(GuysManager, self).get_query_set().filter(gender='M')

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

    def __unicode__(self):
        if self.microntrp:
            un = self.microntrp
        else:
            un = self.ntrp
        return self.first + " " + self.last + ",%3.1f,%4.2f" % (self.ntrp,un)

    def Name(self):
        return self.first + " " + self.last

class SeasonPlayers(models.Model):
    season              = models.ForeignKey(Season)
    player              = models.ForeignKey(Player)
    blockmember         = models.BooleanField()

    objects = BlockManager()

class Couple(models.Model):
    season              = models.ForeignKey(Season)
    name                = models.CharField(max_length=50)
    male                = models.ForeignKey(Player,related_name='guy')
    female              = models.ForeignKey(Player,related_name='gal')
    fulltime            = models.BooleanField()
    canschedule         = models.BooleanField()
    blockcouple         = models.BooleanField()

    def __unicode__(self):
        return  self.name

class Meetings(models.Model):
    season              = models.ForeignKey(Season)
    date                = models.DateField()
    holdout             = models.BooleanField()
    comments            = models.CharField(max_length=128)

class Availability(models.Model):
    meeting             = models.ForeignKey(Meetings)
    player              = models.ForeignKey(Player)
    available           = models.BooleanField()

class Schedule(models.Model):
    meeting             = models.ForeignKey(Meetings)
    player              = models.ForeignKey(Player)
    issub               = models.BooleanField()
    verified            = models.BooleanField()
    partner             = models.ForeignKey(Player,related_name='partner',null=True)

class Slot(models.Model):
    meeting             = models.ForeignKey(Meetings)
    set                 = models.IntegerField()
    court               = models.IntegerField()
    player              = models.ForeignKey(Player)
    position            = models.CharField(max_length=10)

class Matchup(models.Model):
    meeting             = models.ForeignKey(Meetings)
    set                 = models.IntegerField()
    court               = models.IntegerField()
    team1_p1            = models.ForeignKey(Player,related_name="t1_p1",null=True)
    team1_p2            = models.ForeignKey(Player,related_name="t1_p2",null=True)
    team2_p1            = models.ForeignKey(Player,related_name="t2_p1",null=True)
    team2_p2            = models.ForeignKey(Player,related_name="t2_p2",null=True)


