from django.conf.urls import url

from .views import (
    BlockSchedule,
    ScheduleNotify,
)

urlpatterns = (
    url(r'^$', BlockSchedule.as_view(), name='schedule'),
    url(r'^notify/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?',
        ScheduleNotify.as_view(), name="schedule_notify"),
    url(r'^(?P<pk>\d+)/$', BlockSchedule.as_view(), name='season_schedule'),
)
