
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from blockschedule import AvailabilityView

urlpatterns = patterns('api.views',
       url(r'seasons/$',            'getSeasons'),
       url(r'currentseason/$',      'getCurrentSeason'),
       url(r'currentseasondates/$', 'getCurrentSeasonDates'),
       url(r'buzz/$',               'getLatestBuzz'),
       #url(r'ptc/$',                'getPartTimeCouples'),
)
urlpatterns += patterns('api.teams',
       url(r'pickteams/$',          'pickTeams'),
)
urlpatterns += patterns('api.blocksheet',
       url(r'blocksheet/',          'blockSheet'),
       #url(r'blockplayers/$', 'blockschedule.getBlockPlayers'),
)
urlpatterns += patterns('api.blockschedule',
       url(r'blockdates/$',                                 'BlockDates'),

       url(r'subs/(?P<date>\d{4}-\d{1,2}-\d{1,2})$',            'getSubList'),
       url(r'subs/$',                                       'getSubList'),

       url(r'blockplayers/(?P<date>\d{4}-\d{1,2}-\d{1,2})',     'getPlayersForBlock'),
       url(r'blockplayers/',                                'getPlayersForBlock'),

       url(r'blockschedule/(?P<date>\d{4}-\d{1,2}-\d{1,2})',    'blockSchedule'),
       url(r'blockschedule$',                               'blockSchedule'),
       url(r'blockschedule/$',                               'blockSchedule'),
)
urlpatterns += patterns('',
       url(r'availability/$',       AvailabilityView.as_view()),
)

