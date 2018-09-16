from django.apps import AppConfig

class BlockDBConfig(AppConfig):

    name = "blockdb"
    verbose_name = "Block Database App"

    def ready(self):
        super().ready()
        import blockdb.signals
