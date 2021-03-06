from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from blockdb.models import Player


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class TennisUserInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'player'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (TennisUserInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
