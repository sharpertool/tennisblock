from django.contrib import admin
from .models import (Season, Player, SeasonPlayer,
                     Couple, Meeting, Availability,
                     Schedule, Matchup)

class SeasonAdmin(admin.ModelAdmin):
    pass


class PlayerAdmin(admin.ModelAdmin):
    pass


class SeasonPlayerAdmin(admin.ModelAdmin):
    pass


class CoupleAdmin(admin.ModelAdmin):
    pass


class MeetingAdmin(admin.ModelAdmin):
    pass


class AvailabilityAdmin(admin.ModelAdmin):
    pass


class ScheduleAdmin(admin.ModelAdmin):
    pass


class MatchupAdmin(admin.ModelAdmin):
    pass


admin.site.register(Season, SeasonAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(SeasonPlayer, SeasonPlayerAdmin)
admin.site.register(Couple, CoupleAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Availability, AvailabilityAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Matchup, MatchupAdmin)

