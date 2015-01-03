
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import AppConfig

from .models import User, Couple, Season, SeasonPlayers

from api.apiutils import build_meetings_for_season

@receiver(post_save, sender=User)
def user_post_save(sender, instance=None, created=False, **kwargs):
    if created:
        # User Created. do Something helpful
        pass


@receiver(post_save, sender=Season)
def season_post_save(sender, instance=None, created=False, **kwargs):
    if created:
        print("New Season Created... add meetings.")
        build_meetings_for_season(season=instance)


class BlockDBConfig(AppConfig):

    name="blockdb"

    def ready(self):
        pass
