from django.conf.urls import patterns, url

from views import AccountsLogin,\
    AccountsLogout, \
    AcccountsLoginSuccess,\
    AcccountsLogoutSuccess,\
    AcccountsDisabled,\
    AccountsProfile

urlpatterns = patterns('',
                       #url(r'^login/$', AccountsLogin.as_view(),name='login'),
                       url(r'^login/$', 'django.contrib.auth.views.login',name='login'),
                       url(r'^login/success/$', AcccountsLoginSuccess.as_view(),name='login-success'),

                       url(r'^logout/$', AccountsLogout.as_view(),name='logout'),
                       url(r'^logout/success/$', AcccountsLogoutSuccess.as_view(),name='logout-success'),

                       url(r'^profile/$', AccountsProfile.as_view(),name='profile'),
                       url(r'^disabled/$', AcccountsDisabled.as_view(),name='account-disabled'),
)
