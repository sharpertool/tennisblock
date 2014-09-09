from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from views import (
    HomeView,
    BlockSchedule,
    ScheduleNotify,
    AvailabilityView,
    AvailabilityFormView,
    PlaysheetView,
    ContactView,
    AboutView,
    SeasonsView,
    CouplesView
)

urlpatterns = patterns('',
               # Examples:
               url(r'^$', HomeView.as_view(), name='home'),
               url(r'^schedule/notify/(?P<date>\d{4}-\d{1,2}-\d{1,2})/?',
                   ScheduleNotify.as_view(),name="schedule_notify"),
               url(r'^schedule/', BlockSchedule.as_view(),name='schedule'),
               url(r'^availability/', AvailabilityView.as_view(),
                   name='availability'),
               url(r'^availability_form/$', AvailabilityFormView.as_view(),
                   name='availability_form'),
               url(r'^availability_form/(?P<pk>\d+)/?$', AvailabilityFormView.as_view(),
                   name='availability_form_post'),

               url(r'^api/', include('api.urls')),
               url(r'^playsheet/', PlaysheetView.as_view()),
               url(r'^members/', include('members.urls')),
               url(r'^contact/?', ContactView.as_view(),name="contact"),
               url(r'^about/?', AboutView.as_view(),name="about"),
               url(r'^accounts/', include('accounts.urls')),
               url(r'^seasons/$', SeasonsView.as_view(),name="seasons"),
               url(r'^seasons/(?P<pk>\d+)/$', SeasonsView.as_view(),name="season_view"),
               url(r'^couples/(?P<pk>\d+)/$', CouplesView.as_view(),name="couple_editor"),

               # Uncomment the next line to enable the admin:
               url(r'^kag3hewb/', include(admin.site.urls)),
       )
