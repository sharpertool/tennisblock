# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import random
import string

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


from .models import User, Season, Meeting, Player
from api.apiutils import build_meetings_for_season, update_last_meeting_date

@receiver(post_save, sender=User)
def user_post_save(sender, instance=None, created=False, **kwargs):

    if getattr(instance, '_player_create', False):
        return

    try:
        player = instance.player

        changed = False
        if player.first != instance.first_name:
            player.first = instance.first_name
            changed = True
        if player.last != instance.last_name:
            player.last = instance.last_name
            changed = True
        if player.email != instance.email:
            player.email = instance.email
            changed = True

        if changed:
            player.save()
    except:
        """
         I don't do anything in this case. The Player object will be
         created first, and it will save the user.. so I don't want to
         double-save.
        """
        pass


@receiver(post_save, sender=Player)
def player_post_save(sender, instance=None, created=False, **kwargs):
    player = instance

    password_length = 32
    if not player.user:
        # Need to create a new user for this player.
        username = "{}.{}".format(player.first.lower(), player.last.lower())

        try:

            user = get_user_model().objects.get(username=username)
            player.user = user
            player.save()

        except ObjectDoesNotExist:
            email = player.email

            password = ''.join(
                random.choice(string.ascii_uppercase + string.digits)
                for _ in range(password_length))

            now = timezone.now()
            user = get_user_model()(username=username, email=email,
                        is_staff=False, is_active=False,
                        is_superuser=False, last_login=now,
                        first_name=player.first,
                        last_name=player.last,
                        date_joined=now)

            user._player_create = True
            user.save()
            delattr(user, '_player_create')

            user.set_password(password)
            player.user = user
            player.save()

    user = player.user

    # Player updated, sync first,last, email with User
    changed = False
    if player.first != user.first_name:
        user.first_name = player.first
        changed = True
    if player.last != user.last_name:
        user.last_name = player.last
        changed = True
    if player.email != user.email:
        user.email = player.email
        changed = True

    if changed:
        user.save()


@receiver(post_save, sender=Season)
def season_post_save(sender, instance=None, created=False, **kwargs):
    print("Build meetings for season if needed.")
    build_meetings_for_season(season=instance)


@receiver(post_save, sender=Meeting)
def meetings_post_save(sender, instance=None, created=False, **kwargs):
    update_last_meeting_date(instance.season)
