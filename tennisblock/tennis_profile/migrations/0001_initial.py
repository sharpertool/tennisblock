# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TennisUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ntrp', models.FloatField(default=2.5, null=True, blank=True)),
                ('micro_ntrp', models.FloatField(default=2.5, null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True, choices=[(b'F', b'Female'), (b'M', b'Male')])),
                ('phone', models.CharField(max_length=30, null=True, blank=True)),
                ('spouse', models.ForeignKey(to='tennis_profile.TennisUser', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
