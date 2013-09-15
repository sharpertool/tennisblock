
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
       url(r'seasons/$', 'api.views.getSeasons'),
       url(r'currentseason/$', 'api.views.getCurrentSeason'),
       url(r'currentseasondates/$', 'api.views.getCurrentSeasonDates'),
       url(r'buzz/$', 'api.views.getLatestBuzz'),
       url(r'blockplayers/$', 'api.views.getBlockPlayers'),
   )
