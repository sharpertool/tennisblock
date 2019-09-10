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
    path('seasons', get_seasons,
         name='seasons'),
    path('currentseason', get_current_season,
         name='current_season'),
    path('buzz', get_latest_buzz,
         name='buzz'),
    path('pickteams/<date:date>', Teams.as_view(),
         name='pickteams_for_date'),
    path('pickteams', Teams.as_view(),
         name='pickteams'),
    path('blocksheet/<date:date>', blockSheet,
         name='blocksheet_for_date'),
    path('blocksheet', blockSheet,
    name='blocksheet'),
    path('blockdates', BlockDates.as_view(),
         name='blockdates'),
    path('subs/<date:date>', SubsView.as_view(),
            name='subs_for_date'),
    path('subs', SubsView.as_view(),
            name='subs'),
    path('blockplayers/<date:date>',
         BlockPlayers.as_view(),
         name='blockplayers_for_date'),
    path('blockplayers', BlockPlayers.as_view(),
         name='blockplayers'),
    path('blockschedule/', BlockSchedule.as_view(),
         name='blockschedule'),
    path('blockschedule/<date:date>', BlockSchedule.as_view(),
         name='blockschedule_for_date'),
    path('matchdata/<date:date>', MatchData.as_view(),
         name='matchdata_for_date'),
    path('matchdata', MatchData.as_view(),
         name='matchdata'),
    re_path('availability/?', AvailabilityView.as_view(),
            name='availability'),
    path('members/<int:id>', SeasonPlayerView.as_view(),
         name='members_by_date'),
    path('members', SeasonPlayerView.as_view(),
         name='members'),
    path('schedule/notify/<date:date>', BlockNotifyer.as_view(),
         name="schedule_notify"),
    path('couples/', CouplesView.as_view(),
         name='couples'),
    path('couples/<int:season_id>/', CouplesView.as_view(),
         name='couples_for_season'),
)
