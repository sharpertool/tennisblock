from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    AcccountsLoginSuccess,
    AcccountsLogoutSuccess,
    AcccountsDisabled,
    AccountsProfile
)

urlpatterns = [
    path('login/success/',
         AcccountsLoginSuccess.as_view(), name='login-success'),

    path('logout/', auth_views.LogoutView.as_view(),
         {'template_name': 'accounts/logged_out.html'},
         name='logout'),
    path('logout/success/',
         AcccountsLogoutSuccess.as_view(), name='logout-success'),

    path('profile/',
         AccountsProfile.as_view(), name='profile'),
    path('disabled/',
         AcccountsDisabled.as_view(), name='account-disabled'),
]
