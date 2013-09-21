
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
       url(r'seasons/$', 'api.views.getSeasons'),
       url(r'currentseason/$', 'api.views.getCurrentSeason'),
       url(r'currentseasondates/$', 'api.views.getCurrentSeasonDates'),
       url(r'buzz/$', 'api.views.getLatestBuzz'),
       #url(r'blockplayers/$', 'api.blockschedule.getBlockPlayers'),
       url(r'blockdates/$', 'api.blockschedule.BlockDates'),
       url(r'availability/$', 'api.blockschedule.PlayerAvailability'),
       url(r'ptc/$', 'api.views.getPartTimeCouples'),
       url(r'pickteams/$', 'api.teams.pickTeams'),
       url(r'subs/$', 'api.blockschedule.getSubList'),
       url(r'blockplayers/', 'api.blockschedule.getPlayersForBlock'),
       url(r'blocksheet/', 'api.blocksheet.blockSheet'),
       url(r'blockschedule/', 'api.blockschedule.blockSchedule'),
   )

