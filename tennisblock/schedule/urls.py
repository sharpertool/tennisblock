from django.conf.urls import patterns, url

from views import BlockSchedule

urlpatterns = patterns('',
                       url(r'^$', BlockSchedule.as_view()))
