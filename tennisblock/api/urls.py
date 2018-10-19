from django.urls import re_path

from .availability import AvailabilityView
from .members import SeasonPlayerView
from .blocksheet import blockSheet
from .blockschedule import (BlockNotifyer, getBlockDates,
                            getSubList, blockPlayers, blockSchedule,
                            getMatchData)

from .views import getSeasons, getCurrentSeason, getCurrentSeasonDates, getLatestBuzz
from .teams import pick_teams

app_name = 'api'
urlpatterns = (
    re_path(r'seasons/?$', getSeasons),
    re_path(r'currentseason/?$', getCurrentSeason),
    re_path(r'currentseasondates/?$', getCurrentSeasonDates),
    re_path(r'buzz/?$', getLatestBuzz),
    re_path(r'pickteams/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', pick_teams),
    re_path(r'pickteams/?$', pick_teams),
    re_path(r'blocksheet/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', blockSheet),
    re_path(r'blocksheet/?$', blockSheet),
    re_path(r'blockdates/?$', getBlockDates),
    re_path(r'subs/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', getSubList),
    re_path(r'subs/?$', getSubList),
    re_path(r'blockplayers/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', blockPlayers),
    re_path(r'blockplayers/?', blockPlayers),
    re_path(r'blockschedule/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', blockSchedule),
    re_path(r'blockschedule/?$', blockSchedule),
    re_path(r'matchdata/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', getMatchData),
    re_path(r'matchdata/?', getMatchData),
    re_path(r'availability/?$', AvailabilityView.as_view()),
    re_path(r'members/(?P<id>\d+)/?$', SeasonPlayerView.as_view()),
    re_path(r'members/?$', SeasonPlayerView.as_view()),
    re_path(r'schedule/notify/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?',
            BlockNotifyer.as_view(), name="schedule_notify"),
)
