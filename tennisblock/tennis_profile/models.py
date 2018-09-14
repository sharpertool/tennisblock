from django.db import models

from django.contrib.auth.models import User


class TennisUser(models.Model):
    GENDER_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ntrp = models.FloatField(default=2.5, null=True, blank=True)
    micro_ntrp = models.FloatField(default=2.5, null=True, blank=True)
    gender = models.CharField(max_length=1, blank=True,
                              null=True, choices=GENDER_CHOICES)

    phone = models.CharField(max_length=30, null=True, blank=True)
    spouse = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} Gender:{} NTRP:{}".format(
            self.first,
            self.last,
            self.gender,
            self.ntrp)
