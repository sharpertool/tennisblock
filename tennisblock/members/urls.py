from django.conf.urls import patterns, url

from views import ( MembersView,
                    MemberCreate,
                    SeasonPlayersView,
                    SeasonPlayersFormView,
                    SeasonPlayersUpdate)



urlpatterns = patterns('',
                       url(r'^$', SeasonPlayersView.as_view(),name='seasonplayers'),
                       url(r'^form/$', SeasonPlayersFormView.as_view(),name='members_form'),
                       url(r'^update/$', SeasonPlayersUpdate.as_view(),name='members_update'),
                       url(r'^all/$', MembersView.as_view(),name='allplayers'),
                       url(r'^add/$', MemberCreate.as_view(),name='addplayer'),
)
