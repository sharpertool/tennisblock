# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class BlockdbAvailability(models.Model):
    id = models.IntegerField(primary_key=True)
    meeting = models.ForeignKey('BlockdbMeetings')
    player = models.ForeignKey('BlockdbPlayer')
    available = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'blockdb_availability'

class BlockdbCouple(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.ForeignKey('BlockdbSeason')
    name = models.CharField(max_length=50)
    male = models.ForeignKey('BlockdbPlayer')
    female = models.ForeignKey('BlockdbPlayer')
    fulltime = models.IntegerField()
    canschedule = models.IntegerField()
    blockcouple = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'blockdb_couple'

class BlockdbMatchup(models.Model):
    id = models.IntegerField(primary_key=True)
    meeting = models.ForeignKey('BlockdbMeetings')
    set = models.IntegerField()
    court = models.IntegerField()
    team1_p1 = models.ForeignKey('BlockdbPlayer', blank=True, null=True)
    team1_p2 = models.ForeignKey('BlockdbPlayer', blank=True, null=True)
    team2_p1 = models.ForeignKey('BlockdbPlayer', blank=True, null=True)
    team2_p2 = models.ForeignKey('BlockdbPlayer', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'blockdb_matchup'

class BlockdbMeetings(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.ForeignKey('BlockdbSeason')
    date = models.DateField()
    holdout = models.IntegerField()
    comments = models.CharField(max_length=128)
    class Meta:
        managed = False
        db_table = 'blockdb_meetings'

class BlockdbPlayer(models.Model):
    id = models.IntegerField(primary_key=True)
    first = models.CharField(max_length=40)
    last = models.CharField(max_length=60)
    gender = models.CharField(max_length=1)
    ntrp = models.FloatField()
    microntrp = models.FloatField(blank=True, null=True)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=14)
    class Meta:
        managed = False
        db_table = 'blockdb_player'

class BlockdbSchedule(models.Model):
    id = models.IntegerField(primary_key=True)
    meeting = models.ForeignKey(BlockdbMeetings)
    player = models.ForeignKey(BlockdbPlayer)
    issub = models.IntegerField()
    verified = models.IntegerField()
    partner = models.ForeignKey(BlockdbPlayer, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'blockdb_schedule'

class BlockdbSeason(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    courts = models.IntegerField()
    firstcourt = models.IntegerField()
    startdate = models.DateField()
    enddate = models.DateField()
    blockstart = models.DateField()
    blocktime = models.TimeField()
    class Meta:
        managed = False
        db_table = 'blockdb_season'

class BlockdbSeasonplayers(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.ForeignKey(BlockdbSeason)
    player = models.ForeignKey(BlockdbPlayer)
    blockmember = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'blockdb_seasonplayers'

class BlockdbSlot(models.Model):
    id = models.IntegerField(primary_key=True)
    meeting = models.ForeignKey(BlockdbMeetings)
    set = models.IntegerField()
    court = models.IntegerField()
    player = models.ForeignKey(BlockdbPlayer)
    position = models.CharField(max_length=10)
    class Meta:
        managed = False
        db_table = 'blockdb_slot'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'django_site'

class SouthMigrationhistory(models.Model):
    id = models.IntegerField(primary_key=True)
    app_name = models.CharField(max_length=255)
    migration = models.CharField(max_length=255)
    applied = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'south_migrationhistory'

