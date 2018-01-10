from django.apps import AppConfig

class BlockDBConfig(AppConfig):

    name = "blockdb"
    verbose_name = "Block Database App"

    def ready(self):
        import blockdb.signals
        super(BlockDBConfig, self).ready()
