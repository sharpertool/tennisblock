from django.urls import path, re_path, register_converter

from .availability import AvailabilityView
from .members import SeasonPlayerView
from .blocksheet import blockSheet
from .blockschedule import (BlockNotifyer, getBlockDates,
                            getSubList, blockPlayers, blockSchedule,
                            getMatchData, clear_schedule)

from .views import get_seasons, get_current_season, get_latest_buzz
from .teams import Teams

from . import converters

register_converter(converters.BlockDateConverter, 'date')

app_name = 'api'
urlpatterns = (
    path('seasons', get_seasons),
    path('currentseason', get_current_season),
    path('buzz', get_latest_buzz),
    path('pickteams/<date:date>', Teams.as_view()),
    path('pickteams', Teams.as_view()),
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
    path('availability/', AvailabilityView.as_view()),
    path('members/<int:id>', SeasonPlayerView.as_view()),
    path('members', SeasonPlayerView.as_view()),
    path('schedule', clear_schedule),
    path('schedule/notify/<date:date>', BlockNotifyer.as_view(), name="schedule_notify"),
)
