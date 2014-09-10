from django.conf.urls import patterns, url

from views import (
    AcccountsLoginSuccess,
    AcccountsLogoutSuccess,
    AcccountsDisabled,
    AccountsProfile
)

urlpatterns = patterns('',
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           {'template_name':'accounts/login.html'},
                           name='login'),
                       url(r'^login/success/$',
                           AcccountsLoginSuccess.as_view(),name='login-success'),

                       #url(r'^logout/$', AccountsLogout.as_view(),name='logout'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'template_name':'accounts/logged_out.html'},
                           name='logout'),
                       url(r'^logout/success/$',
                           AcccountsLogoutSuccess.as_view(),name='logout-success'),

                       url(r'^profile/$',
                           AccountsProfile.as_view(),name='profile'),
                       url(r'^disabled/$',
                           AcccountsDisabled.as_view(),name='account-disabled'),
)
