from django.apps import AppConfig


class MembersConfig(AppConfig):
    name = "members"
    verbose_name = "Members App Config"

    def ready(self):
        super().ready()
        import members.signals
