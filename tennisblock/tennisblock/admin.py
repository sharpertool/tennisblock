
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from tennis_profile.models import TennisUser
from blockdb.models import Player,SeasonPlayers,Couple,Meetings,Matchup,Season


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class TennisUserInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'player'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (TennisUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Player)
admin.site.register(SeasonPlayers)
admin.site.register(Meetings)
admin.site.register(Season)

print("Admin was called.")
