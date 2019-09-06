from django.urls import path, re_path, register_converter

from .availability import AvailabilityView
from .members import SeasonPlayerView
from .blocksheet import blockSheet
from .blockschedule import (BlockNotifyer,
                            SubsView, BlockPlayers,
                            MatchData, BlockSchedule,
                            BlockDates)


from .views.season import get_seasons, get_current_season, get_latest_buzz, CouplesView
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
    path('blockdates', BlockDates.as_view()),
    re_path('subs/<date:date>/?', SubsView.as_view()),
    re_path('subs/?', SubsView.as_view()),
    path('blockplayers/<date:date>', BlockPlayers.as_view()),
    path('blockplayers', BlockPlayers.as_view()),
    path('blockschedule/', BlockSchedule.as_view()),
    path('blockschedule/<date:date>', BlockSchedule.as_view()),
    path('matchdata/<date:date>', MatchData.as_view()),
    path('matchdata', MatchData.as_view()),
    re_path('availability/?', AvailabilityView.as_view()),
    path('members/<int:id>', SeasonPlayerView.as_view()),
    path('members', SeasonPlayerView.as_view()),
    path('schedule/notify/<date:date>', BlockNotifyer.as_view(), name="schedule_notify"),
    path('couples/', CouplesView.as_view(), name='couples')
)
