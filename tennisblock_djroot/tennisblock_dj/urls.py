from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tennisblock.views import HomeView
from schedule.views import ScheduleView
from about.views import AboutView
from contact.views import ContactView
from availability.views import AvailabilityView
from members.views import MembersView
from playsheet.views import PlaysheetView

urlpatterns = patterns('',
               # Examples:
               url(r'^$', HomeView.as_view()),
               # url(r'^$', 'tennisblock_dj.views.home', name='home'),
               # url(r'^tennisblock_project/', include('tennisblock_dj.foo.urls')),
               url(r'^api/', include('api.urls')),

               url(r'^schedule/', ScheduleView.as_view()),
               url(r'^availability/', AvailabilityView.as_view()),
               url(r'^playsheet/', PlaysheetView.as_view()),
               url(r'^members/', MembersView.as_view()),
               url(r'^contact/', ContactView.as_view()),
               url(r'^about/', AboutView.as_view()),

               # Uncomment the admin/doc line below to enable admin documentation:
               url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

               # Uncomment the next line to enable the admin:
               url(r'^admin/', include(admin.site.urls)),
               )
