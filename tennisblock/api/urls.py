from django.urls import path, re_path, register_converter

from .availability import AvailabilityView
from .members import SeasonPlayerView
from .blocksheet import blockSheet
from .blockschedule import (BlockNotifyer, getBlockDates,
                            getSubList, blockPlayers, blockSchedule,
                            getMatchData)

from .views import getSeasons, getCurrentSeason, getCurrentSeasonDates, getLatestBuzz
from .teams import pick_teams

from . import converters

register_converter(converters.BlockDateConverter, 'date')

app_name = 'api'
urlpatterns = (
    re_path('seasons/?', getSeasons),
    re_path('currentseason/?', getCurrentSeason),
    re_path('currentseasondates/?', getCurrentSeasonDates),
    re_path('buzz/?', getLatestBuzz),
    re_path('pickteams/<date:date>/?', pick_teams),
    re_path('pickteams/?', pick_teams),
    re_path('blocksheet/<date:date>/?', blockSheet),
    re_path('blocksheet/?', blockSheet),
    re_path('blockdates/?', getBlockDates),
    re_path('subs/<date:date>/?', getSubList),
    re_path('subs/?', getSubList),
    re_path('blockplayers/<date:date>/?', blockPlayers),
    re_path('blockplayers/?', blockPlayers),
    re_path('blockschedule/<date:date>/?', blockSchedule),
    re_path('blockschedule/?', blockSchedule),
    re_path('matchdata/<date:date>/?', getMatchData),
    re_path('matchdata/?', getMatchData),
    re_path('availability/?', AvailabilityView.as_view()),
    re_path('members/<int:id>/?', SeasonPlayerView.as_view()),
    re_path('members/?', SeasonPlayerView.as_view()),
    re_path('schedule/notify/<date:date>/?', BlockNotifyer.as_view(), name="schedule_notify"),
)
