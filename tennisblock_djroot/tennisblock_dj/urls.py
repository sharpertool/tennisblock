from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tennisblock.views import HomeView

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', HomeView.as_view()),
                       # url(r'^$', 'tennisblock_dj.views.home', name='home'),
                       # url(r'^tennisblock_project/', include('tennisblock_dj.foo.urls')),
                       url(r'^api/', include('api.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       )
