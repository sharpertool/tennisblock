import django.dispatch


player_created = django.dispatch.Signal(providing_args=["player", "request"])
player_updated = django.dispatch.Signal(providing_args=["player", "request"])
player_deleted = django.dispatch.Signal(providing_args=["player", "request"])
