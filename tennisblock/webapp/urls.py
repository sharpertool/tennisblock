from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls

from .views import (
    HomeView,
    AvailabilityView,
    AvailabilityFormView,
    PlaysheetView,
    ContactView,
    AboutView,
)

urlpatterns = [
    path('confirmation/', include('confirm.urls', namespace='confirmation')),
    path('', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('availability/', include('availability.urls', namespace='availability')),
    path('playsheet/', PlaysheetView.as_view()),
    path('accounts/', include('accounts.urls')),
    path('contact/', ContactView.as_view(), name="contact"),
    path('season/', include('season.urls')),
    path('members/', include('members.urls')),
    path('schedule/', include('schedule.urls', namespace='schedule')),
    path('api/', include('api.urls')),
    path('django-admin/', admin.site.urls),
    path('chat/', include('tennis_channels.urls', namespace='chat')),

    path('admin/', include(wagtailadmin_urls)),
    path('', include(wagtail_urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns