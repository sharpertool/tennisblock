from django.urls import re_path, path

from .views import (
    ScheduleConfirmed,
    ScheduleRejected,
    ScheduleRejectedComplete
)

app_name = 'confirm'
urlpatterns = (
    path('<uuid:code>/confirmed',
         ScheduleConfirmed.as_view(), name='confirm'),
    path('<uuid:code>/rejected',
         ScheduleRejected.as_view(), name='reject'),
    path('<uuid:code>/rejected/done',
         ScheduleRejectedComplete.as_view(), name='reject_done'),
)
