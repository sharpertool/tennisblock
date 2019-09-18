from django.apps import AppConfig


class ConfirmConfig(AppConfig):
    name = 'confirm'

    def ready(self):
        super().ready()
        import confirm.signals
