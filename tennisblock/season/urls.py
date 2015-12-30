from django.conf.urls import url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from .views import (
    SeasonsView,
    SeasonDetailView,
    SeasonCreate,
)

urlpatterns = [
    url(r'^$', SeasonsView.as_view(), name="seasons"),
    url(r'^(?P<pk>\d+)/$', SeasonDetailView.as_view(), name="season_detail"),
    url(r'^create/', SeasonCreate.as_view(), name='create_season'),
]
