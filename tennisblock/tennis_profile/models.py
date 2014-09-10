from django.db import models

from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TennisUser(models.Model):
    GENDER_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
    )
    user = models.OneToOneField(User)
    ntrp = models.FloatField(default=2.5,null=True,blank=True)
    micro_ntrp = models.FloatField(default=2.5,null=True,blank=True)
    gender = models.CharField(max_length=1,blank=True,
                              null=True,choices=GENDER_CHOICES)

    phone = models.CharField(max_length=30,null=True,blank=True)
    spouse = models.ForeignKey("self",null=True,blank=True)

    def __str__(self):
        return "{} {} Gender:{} NTRP:{}".format(self.user.first_name,
                              self.user.last_name,
                              self.gender,self.ntrp)

