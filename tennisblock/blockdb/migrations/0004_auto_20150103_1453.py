# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0003_auto_20140910_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='lastdate',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='player',
            field=models.ForeignKey(related_name='available', to='blockdb.Player', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='couple',
            name='female',
            field=models.ForeignKey(related_name='couple_gal', to='blockdb.Player', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='couple',
            name='male',
            field=models.ForeignKey(related_name='couple_guy', to='blockdb.Player', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='partner',
            field=models.ForeignKey(related_name='scheduled_partner', to='blockdb.Player', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='player',
            field=models.ForeignKey(related_name='scheduled', to='blockdb.Player', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seasonplayers',
            name='season',
            field=models.ForeignKey(related_name='players', to='blockdb.Season', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
