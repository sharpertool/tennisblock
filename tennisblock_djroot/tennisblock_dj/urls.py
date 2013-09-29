from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tennisblock.views import HomeView
from about.views import AboutView
from contact.views import ContactView
from availability.views import AvailabilityView
from playsheet.views import PlaysheetView

urlpatterns = patterns('',
               # Examples:
               url(r'^$', HomeView.as_view()),
               url(r'^api/', include('api.urls')),
               url(r'^schedule/', include('schedule.urls')),
               url(r'^availability/', AvailabilityView.as_view()),
               url(r'^playsheet/', PlaysheetView.as_view()),
               url(r'^members/', include('members.urls')),
               url(r'^contact/', ContactView.as_view()),
               url(r'^about/', AboutView.as_view()),

               # Uncomment the admin/doc line below to enable admin documentation:
               url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

               # Uncomment the next line to enable the admin:
               url(r'^admin/', include(admin.site.urls)),
       )
