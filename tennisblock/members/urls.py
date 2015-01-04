from django.conf.urls import patterns, url

from views import (MembersView, MemberCreate,
                    PlayersView, PlayerList, PlayerDetail, PlayerUpdate, DeletePlayerView,
                    SeasonPlayersFormView, SeasonPlayersUpdate)



urlpatterns = patterns('',
                       url(r'^$', MembersView.as_view(), name='seasonplayers'),
                       url(r'^form/$', SeasonPlayersFormView.as_view(), name='members_form'),
                       url(r'^update/$', SeasonPlayersUpdate.as_view(), name='members_update'),
                       url(r'^player/list/$', PlayerList.as_view(), name='player_list'),
                       url(r'^player/(?P<pk>\d+)/detail/$', PlayerDetail.as_view(), name='player_detail'),
                       url(r'^player/(?P<pk>\d+)/update/$', PlayerUpdate.as_view(), name='player_update'),
                       url(r'^player/(?P<pk>\d+)/delete/$', DeletePlayerView.as_view(), name='player_delete'),
                       url(r'^add/$', MemberCreate.as_view(), name='addplayer'),
)
