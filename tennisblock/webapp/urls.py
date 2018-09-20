from django.urls import include, re_path

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

urlpatterns = (
    # Examples:
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^availability/', AvailabilityView.as_view(), name='availability'),
    re_path(r'^availability_form/$', AvailabilityFormView.as_view(), name='availability_form'),
    re_path(r'^availability_form/(?P<pk>\d+)/?$', AvailabilityFormView.as_view(), name='availability_form_post'),
    re_path(r'^playsheet/', PlaysheetView.as_view()),
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^couples/(?P<pk>\d+)/$', CouplesView.as_view(), name="couple_editor"),
    re_path(r'^contact/?', ContactView.as_view(), name="contact"),
    re_path(r'^about/?', AboutView.as_view(), name="about"),
    re_path(r'^season/', include('season.urls')),
    re_path(r'^members/', include('members.urls')),
    re_path(r'^schedule/', include('schedule.urls')),
    re_path(r'^api/', include('api.urls')),
    re_path(r'^django-admin/', admin.site.urls),
)
