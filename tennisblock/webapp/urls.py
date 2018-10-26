from django.urls import include, path
from django.contrib import admin

from .views import (
    HomeView,
    AvailabilityView,
    AvailabilityFormView,
    PlaysheetView,
    ContactView,
    AboutView,
    CouplesView
)

urlpatterns = (
    # Examples:
    path('', HomeView.as_view(), name='home'),
    path('availability/', AvailabilityView.as_view(), name='availability'),
    path('availability_form/', AvailabilityFormView.as_view(), name='availability_form'),
    path('availability_form/<int:pk>/', AvailabilityFormView.as_view(), name='availability_form_post'),
    path('playsheet/', PlaysheetView.as_view()),
    path('accounts/', include('accounts.urls')),
    path('couples/<int:pk>>', CouplesView.as_view(), name="couple_editor"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('about/', AboutView.as_view(), name="about"),
    path('season/', include('season.urls')),
    path('members/', include('members.urls')),
    path('schedule/', include('schedule.urls')),
    path('api/', include('api.urls')),
    path('django-admin/', admin.site.urls),
)
