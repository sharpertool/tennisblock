from django.urls import re_path
import django.contrib.auth.views

from .views import (
    AcccountsLoginSuccess,
    AcccountsLogoutSuccess,
    AcccountsDisabled,
    AccountsProfile
)

urlpatterns = [
    re_path(r'^login/$', django.contrib.auth.views.login,
            {'template_name': 'accounts/login.html'}, name='login'),
    re_path(r'^login/success/$',
            AcccountsLoginSuccess.as_view(), name='login-success'),

    re_path(r'^logout/$', django.contrib.auth.views.logout,
            {'template_name': 'accounts/logged_out.html'},
            name='logout'),
    re_path(r'^logout/success/$',
            AcccountsLogoutSuccess.as_view(), name='logout-success'),

    re_path(r'^profile/$',
            AccountsProfile.as_view(), name='profile'),
    re_path(r'^disabled/$',
            AcccountsDisabled.as_view(), name='account-disabled'),
]
