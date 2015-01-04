
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import AppConfig

from .models import User, Season, Meetings, Player

from api.apiutils import build_meetings_for_season, update_last_meeting_date

@receiver(post_save, sender=User)
def user_post_save(sender, instance=None, created=False, **kwargs):
    if created:
        # When a user object is created, create the associated player object.
        p = Player(
            user=instance,
            first=instance.first_name,
            last=instance.last_name,
            email=instance.email
        )
        p.save()
    else:
        # User updated, sync first,last, email with Player
        pass


@receiver(post_save, sender=Player)
def player_post_save(sender, instance=None, created=False, **kwargs):
    if created:
        # Player Created. do Something helpful
        pass
    else:
        # Player updated, sync first,last, email with User
        pass


@receiver(post_save, sender=Season)
def season_post_save(sender, instance=None, created=False, **kwargs):
    if created:
        print("New Season Created... add meetings.")
        build_meetings_for_season(season=instance)

@receiver(post_save, sender=Meetings)
def meetings_post_save(sender, instance=None, created=False, **kwargs):
    update_last_meeting_date(instance.season)

class BlockDBConfig(AppConfig):

    name="blockdb"

    def ready(self):
        pass
