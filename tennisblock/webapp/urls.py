from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views

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
    path('', auth_views.LoginView.as_view(template_name='home.html'), name='login'),
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
