# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import string

from django.conf import settings
from django.utils import timezone
from django.db import models, migrations

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
def create_user_accounts(apps,schemea_editor):

    Player = apps.get_model('blockdb','Player')
    User = apps.get_model('auth','User')

    password_length = 32

    for player in Player.objects.all():
        if not player.user:
            # Need to create a new user for this player.
            username = "{}.{}".format(player.first.lower(), player.last.lower())

            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                email = player.user.email

                password = ''.join(
                    random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(password_length))

                now = timezone.now()
                user = User(username=username, email=email,
                            is_staff=False, is_active=False,
                            is_superuser=False, last_login=now,
                            first_name=player.first,
                            last_name=player.last,
                            date_joined=now)

                #user.set_password(password)
                user.save()

            player.user = user
            player.save()



class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0002_player_user'),
    ]

    operations = [
        migrations.RunPython(create_user_accounts),
    ]
