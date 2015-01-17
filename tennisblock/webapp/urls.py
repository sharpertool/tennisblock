from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from .views import (
    HomeView,
    AvailabilityView,
    AvailabilityFormView,
    PlaysheetView,
    ContactView,
    AboutView,
    CouplesView
)

urlpatterns = patterns('',
               # Examples:
               url(r'^$', HomeView.as_view(), name='home'),

               url(r'^availability/', AvailabilityView.as_view(),
                   name='availability'),
               url(r'^availability_form/$', AvailabilityFormView.as_view(),
                   name='availability_form'),
               url(r'^availability_form/(?P<pk>\d+)/?$', AvailabilityFormView.as_view(),
                   name='availability_form_post'),

               url(r'^playsheet/', PlaysheetView.as_view()),
               url(r'^accounts/', include('accounts.urls')),
               url(r'^couples/(?P<pk>\d+)/$', CouplesView.as_view(), name="couple_editor"),
               url(r'^contact/?', ContactView.as_view(), name="contact"),
               url(r'^about/?', AboutView.as_view(), name="about"),

               url(r'^season/', include('season.urls')),
               url(r'^members/', include('members.urls')),
               url(r'^schedule/', include('schedule.urls')),
               url(r'^api/', include('api.urls')),

               # Uncomment the next line to enable the admin:
               url(r'^kag3hewb/', include(admin.site.urls)),
       )
