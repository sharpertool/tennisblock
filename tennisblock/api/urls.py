from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
from availability import AvailabilityView
from members import SeasonPlayersView
from blockschedule import BlockNotifyer

urlpatterns = patterns('api.views',
                       url(r'seasons/?$', 'getSeasons'),
                       url(r'currentseason/?$', 'getCurrentSeason'),
                       url(r'currentseasondates/?$', 'getCurrentSeasonDates'),
                       url(r'buzz/?$', 'getLatestBuzz'),
                       #url(r'ptc/$',                'getPartTimeCouples'),
)
urlpatterns += patterns('api.teams',
                        url(r'pickteams/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', 'pickTeams'),
                        url(r'pickteams/?$', 'pickTeams'),
)
urlpatterns += patterns('api.blocksheet',
                        url(r'blocksheet/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', 'blockSheet'),
                        url(r'blocksheet/?$', 'blockSheet'),
                        url(r'blocksheet2/?$', 'blockSheetReportlab'),
                        #url(r'blockplayers/$', 'blockschedule.getBlockPlayers'),
)
urlpatterns += patterns('api.blockschedule',
                        url(r'blockdates/?$', 'getBlockDates'),

                        url(r'subs/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?$', 'getSubList'),
                        url(r'subs/?$', 'getSubList'),

                        url(r'blockplayers/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', 'blockPlayers'),
                        url(r'blockplayers/?', 'blockPlayers'),

                        url(r'blockschedule/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', 'blockSchedule'),
                        url(r'blockschedule/?$', 'blockSchedule'),

                        url(r'matchdata/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?', 'getMatchData'),
                        url(r'matchdata/?', 'getMatchData'),
)
urlpatterns += patterns('',
                        url(r'availability/?$', AvailabilityView.as_view()),
)
urlpatterns += patterns('api.members',
                        url(r'members/(?P<id>\d+)/?$', SeasonPlayersView.as_view()),
                        url(r'members/?$', SeasonPlayersView.as_view()),
)

urlpatterns += patterns('',
                        url(r'schedule/notify/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?',
                            BlockNotifyer.as_view(),name="schedule_notify")
)

