from django.conf.urls import url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
from availability import AvailabilityView
from members import SeasonPlayersView
from blockschedule import BlockNotifyer

from .views import getSeasons, getCurrentSeason, getCurrentSeasonDates, getLatestBuzz
from .teams import pickTeams
from .blocksheet import blockSheet
from .blockschedule import getBlockDates, getSubList, blockPlayers, blockSchedule, getMatchData

urlpatterns = (
    url(r'seasons/?$', getSeasons, prefix='api.views'),
    url(r'currentseason/?$', getCurrentSeason, prefix='api.views'),
    url(r'currentseasondates/?$', getCurrentSeasonDates, prefix='api.views'),
    url(r'buzz/?$', getLatestBuzz, prefix='api.views'),
)

urlpatterns += (
    url(r'pickteams/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', pickTeams, prefix='api.teams'),
    url(r'pickteams/?$', pickTeams, prefix='api.teams'),
)

urlpatterns += (
    url(r'blocksheet/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', blockSheet, prefix='api.blocksheet'),
    url(r'blocksheet/?$', blockSheet, prefix='api.blocksheet'),
)

urlpatterns += (
    url(r'blockdates/?$', getBlockDates, prefix='api.blockschedule'),

    url(r'subs/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', getSubList, prefix='api.blockschedule'),
    url(r'subs/?$', getSubList, prefix='api.blockschedule'),

    url(r'blockplayers/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', blockPlayers, prefix='api.blockschedule'),
    url(r'blockplayers/?', blockPlayers, prefix='api.blockschedule'),

    url(r'blockschedule/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', blockSchedule, prefix='api.blockschedule'),
    url(r'blockschedule/?$', blockSchedule, prefix='api.blockschedule'),

    url(r'matchdata/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', getMatchData, prefix='api.blockschedule'),
    url(r'matchdata/?', getMatchData, prefix='api.blockschedule'),
)

urlpatterns += (
    url(r'availability/?$', AvailabilityView.as_view()),
)

urlpatterns += (
    url(r'members/(?P<id>\d+)/?$', SeasonPlayersView.as_view(), prefix='api.members'),
    url(r'members/?$', SeasonPlayersView.as_view(), prefix='api.members'),
)

urlpatterns += (
    url(r'schedule/notify/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?',
        BlockNotifyer.as_view(), name="schedule_notify"),
)
