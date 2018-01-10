from django.conf.urls import url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
from .availability import AvailabilityView
from .members import SeasonPlayersView
from .blockschedule import BlockNotifyer

from .views import getSeasons, getCurrentSeason, getCurrentSeasonDates, getLatestBuzz
from .teams import pickTeams
from .blocksheet import blockSheet
from .blockschedule import getBlockDates, getSubList, blockPlayers, blockSchedule, getMatchData

urlpatterns = (
    url(r'seasons/?$', getSeasons),
    url(r'currentseason/?$', getCurrentSeason),
    url(r'currentseasondates/?$', getCurrentSeasonDates),
    url(r'buzz/?$', getLatestBuzz),
)

urlpatterns += (
    url(r'pickteams/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', pickTeams),
    url(r'pickteams/?$', pickTeams),
)

urlpatterns += (
    url(r'blocksheet/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', blockSheet),
    url(r'blocksheet/?$', blockSheet),
)

urlpatterns += (
    url(r'blockdates/?$', getBlockDates),

    url(r'subs/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', getSubList),
    url(r'subs/?$', getSubList),

    url(r'blockplayers/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', blockPlayers),
    url(r'blockplayers/?', blockPlayers),

    url(r'blockschedule/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', blockSchedule),
    url(r'blockschedule/?$', blockSchedule),

    url(r'matchdata/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', getMatchData),
    url(r'matchdata/?', getMatchData),
)

urlpatterns += (
    url(r'availability/?$', AvailabilityView.as_view()),
)

urlpatterns += (
    url(r'members/(?P<id>\d+)/?$', SeasonPlayersView.as_view()),
    url(r'members/?$', SeasonPlayersView.as_view()),
)

urlpatterns += (
    url(r'schedule/notify/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?',
        BlockNotifyer.as_view(), name="schedule_notify"),
)
