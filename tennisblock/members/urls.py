from django.conf.urls import url

from .views import (MembersView, PlayerListView, PlayerDetailView,
                    PlayerUpdateView, PlayerDeleteView,
                    PlayerCreateView, SeasonPlayerFormView, SeasonPlayerUpdate)

urlpatterns = [
    url(r'^$', MembersView.as_view(), name='seasonplayers'),
    url(r'^form/$', SeasonPlayerFormView.as_view(), name='members_form'),
    url(r'^update/$', SeasonPlayerUpdate.as_view(), name='members_update'),
    url(r'^player/list/$', PlayerListView.as_view(), name='player_list'),
    url(r"^player/create/$", PlayerCreateView.as_view(), name="player_create"),
    url(r'^player/(?P<pk>\d+)/detail/$', PlayerDetailView.as_view(), name='player_detail'),
    url(r'^player/(?P<pk>\d+)/update/$', PlayerUpdateView.as_view(), name='player_update'),
    url(r'^player/(?P<pk>\d+)/delete/$', PlayerDeleteView.as_view(), name='player_delete'),
    url(r'^add/$', PlayerCreateView.as_view(), name='addplayer'),
]
