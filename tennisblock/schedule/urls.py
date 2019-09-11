from django.urls import re_path, path

from .views import (
    BlockSchedule,
    ScheduleNotify,
    ScheduleConfirm,
    ScheduleConfirmed,
    ScheduleRejected,
)

app_name = 'schedule'
urlpatterns = (
    re_path(r'^notify/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?',
            ScheduleNotify.as_view(), name="schedule_notify"),
    re_path('confirm/<uuid:code>/?', ScheduleConfirm.as_view(), name='confirm'),
    path('response/confirmed/',
         ScheduleConfirmed.as_view(), name='response_confirmed'),
    path('response/rejected/',
         ScheduleRejected.as_view(), name='response_rejected'),
    re_path(r'(?P<date>\d{4}-\d{1,2}-\d{1,2})?', BlockSchedule.as_view(), name='schedule'),
    re_path(r'^(?P<pk>\d+)/$', BlockSchedule.as_view(), name='season_schedule'),
)
