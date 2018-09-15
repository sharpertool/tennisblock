from django.conf.urls import url

from .views import (MembersView, MemberCreate,
                   PlayerList, PlayerDetail, PlayerUpdate, DeletePlayerView,
                   CreatePlayerView, SeasonPlayerFormView, SeasonPlayerUpdate)

urlpatterns = [
    url(r'^$', MembersView.as_view(), name='seasonplayers'),
    url(r'^form/$', SeasonPlayerFormView.as_view(), name='members_form'),
    url(r'^update/$', SeasonPlayerUpdate.as_view(), name='members_update'),
    url(r'^player/list/$', PlayerList.as_view(), name='player_list'),
    url(r"^player/create/$", CreatePlayerView.as_view(), name="player_create"),
    url(r'^player/(?P<pk>\d+)/detail/$', PlayerDetail.as_view(), name='player_detail'),
    url(r'^player/(?P<pk>\d+)/update/$', PlayerUpdate.as_view(), name='player_update'),
    url(r'^player/(?P<pk>\d+)/delete/$', DeletePlayerView.as_view(), name='player_delete'),
    url(r'^add/$', MemberCreate.as_view(), name='addplayer'),
]
