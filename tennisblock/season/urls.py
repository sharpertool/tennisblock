from django.urls import re_path, path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from .views import (
    SeasonsView,
    SeasonDetailView,
    SeasonCreate,
    CouplesView
)

app_name = 'season'
urlpatterns = [
    re_path(r'^$', SeasonsView.as_view(), name="seasons"),
    re_path(r'^(?P<pk>\d+)/$', SeasonDetailView.as_view(), name="season_detail"),
    re_path(r'^create/', SeasonCreate.as_view(), name='create_season'),
    path('<int:pk>/couples/', CouplesView.as_view(), name="couple_editor")
]
