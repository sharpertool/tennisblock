from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tennisblock.views import HomeView
from tennisblock.about.views import AboutView
from tennisblock.contact.views import ContactView
from tennisblock.availability.views import AvailabilityView
from tennisblock.playsheet.views import PlaysheetView

urlpatterns = patterns('',
               # Examples:
               url(r'^$', HomeView.as_view()),
               url(r'^api/', include('tennisblock.api.urls')),
               url(r'^schedule/', include('tennisblock.schedule.urls')),
               url(r'^availability/', AvailabilityView.as_view()),
               url(r'^playsheet/', PlaysheetView.as_view()),
               url(r'^members/', include('tennisblock.members.urls')),
               url(r'^contact/?', ContactView.as_view()),
               url(r'^about/?', AboutView.as_view()),
               url(r'^accounts/', include('tennisblock.accounts.urls')),

               # Uncomment the admin/doc line below to enable admin documentation:
               #url(r'^kag3hewb/doc/', include('django.contrib.admindocs.urls')),

               # Uncomment the next line to enable the admin:
               url(r'^kag3hewb/', include(admin.site.urls)),
       )
