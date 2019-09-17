from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    name = "schedule"

    def ready(self):
        super().ready()
        import schedule.signals
