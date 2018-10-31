from django.urls import path, register_converter

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
    path('seasons', getSeasons),
    path('currentseason', getCurrentSeason),
    path('currentseasondates', getCurrentSeasonDates),
    path('buzz', getLatestBuzz),
    path('pickteams/<date:date>', pick_teams),
    path('pickteams', pick_teams),
    path('blocksheet/<date:date>', blockSheet),
    path('blocksheet', blockSheet),
    path('blockdates', getBlockDates),
    path('subs/<date:date>', getSubList),
    path('subs', getSubList),
    path('blockplayers/<date:date>', blockPlayers),
    path('blockplayers', blockPlayers),
    path('blockschedule/<date:date>', blockSchedule),
    path('blockschedule', blockSchedule),
    path('matchdata/<date:date>', getMatchData),
    path('matchdata', getMatchData),
    path('availability', AvailabilityView.as_view()),
    path('members/<int:id>', SeasonPlayerView.as_view()),
    path('members', SeasonPlayerView.as_view()),
    path('schedule/notify/<date:date>', BlockNotifyer.as_view(), name="schedule_notify"),
)
