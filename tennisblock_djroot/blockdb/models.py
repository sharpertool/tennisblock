from django.db import models

# Create your models here.


class Season(models.Model):
     season             = models.CharField(max_length=20)
     courts             = models.IntegerField()
     firstcourt         = models.IntegerField()

class Player(models.Model):
    first               = models.CharField(max_length=40)
    last                = models.CharField(max_length=60)
    gender              = models.CharField(max_length=1)
    ntrp                = models.FloatField()
    microntrp           = models.FloatField()
    email               = models.CharField(max_length=50)
    phone               = models.CharField(max_length=14)

class Couple(models.Model):
    season              = models.ForeignKey(Season)
    name                = models.CharField(max_length=50)
    male                = models.ForeignKey(Player)
    female              = models.ForeignKey(Player)
    fulltime            = models.BooleanField()
    canschedule         = models.BooleanField()
    blockcouple         = models.BooleanField()

class Meetings(models.Model):
    season              = models.ForeignKey(Season)
    date                = models.DateField()
    holdout             = models.BooleanField()
    comments            = models.CharField(max_length=128)

class Availability(models.Model):
    meeting             = models.ForeignKey(Meetings)
    player              = models.ForeignKey(Player)
    available           = models.BooleanField()

class SeasonPlayers(models.Model):
    season              = models.ForeignKey(Season)
    player              = models.ForeignKey(Player)
    blockmember         = models.BooleanField()
