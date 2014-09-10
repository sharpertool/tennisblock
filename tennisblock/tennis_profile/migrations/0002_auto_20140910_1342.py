# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tennisuser',
            name='spouse',
            field=models.ForeignKey(blank=True, to='tennis_profile.TennisUser', null=True),
        ),
    ]
