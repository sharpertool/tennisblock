# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def migrate_names(apps, schema_editor):

    Player = apps.get_model('blockdb', 'Player')

    for player in Player.objects.all():
        u = player.user
        changed = False
        if u.first_name != player.first:
            u.first_name = player.first
            changed = True

        if u.last_name != player.last:
            u.last_name = player.last
            changed = True

        if u.email != player.email:
            u.email = player.email
            changed = True

        if changed:
            u.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0004_auto_20150103_1453'),
    ]

    operations = [
        migrations.RunPython(migrate_names),
    ]
