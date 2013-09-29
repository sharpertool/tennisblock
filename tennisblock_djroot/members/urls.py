from django.conf.urls import patterns, url

from views import MembersView,MemberCreate,SeasonPlayersView

urlpatterns = patterns('',
                       url(r'^$', SeasonPlayersView.as_view(),name='seasonplayers'),
                       url(r'^all/$', MembersView.as_view(),name='allplayers'),
                       url(r'^add/$', MemberCreate.as_view(),name='addplayer'),
)
