from django.urls import re_path

from .views import (MembersView, MembersViewAngular, MembersViewReact,
                    PlayerListView, PlayerDetailView,
                    PlayerUpdateView, PlayerDeleteView,
                    PlayerCreateView, SeasonPlayerFormView,
                    SeasonPlayerUpdate)

app_name = 'members'
urlpatterns = [
    re_path(r'^$', MembersViewAngular.as_view(), name='seasonplayers'),
    re_path(r'^blockmembers/$', MembersView.as_view(), name='block'),
    re_path(r'^react/$', MembersViewReact.as_view(), name='block_react'),
    re_path(r'^form/$', SeasonPlayerFormView.as_view(), name='members_form'),
    re_path(r'^update/$', SeasonPlayerUpdate.as_view(), name='members_update'),
    re_path(r'^player/list/$', PlayerListView.as_view(), name='player_list'),
    re_path(r"^player/create/$", PlayerCreateView.as_view(), name="player_create"),
    re_path(r'^player/(?P<pk>\d+)/detail/$', PlayerDetailView.as_view(), name='player_detail'),
    re_path(r'^player/(?P<pk>\d+)/update/$', PlayerUpdateView.as_view(), name='player_update'),
    re_path(r'^player/(?P<pk>\d+)/delete/$', PlayerDeleteView.as_view(), name='player_delete'),
    re_path(r'^add/$', PlayerCreateView.as_view(), name='addplayer'),
]
