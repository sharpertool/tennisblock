from django.urls import path

from .views import (AvailabilityView, AvailabilityAngularView, AvailabilityFormView)

app_name = 'availability'
urlpatterns = (
    path('', AvailabilityView.as_view(), name="main"),
    path(r'angular/', AvailabilityAngularView.as_view(), name="angular"),
    path('availability_form/', AvailabilityFormView.as_view(), name='form'),
    path('availability_form/<int:pk>/', AvailabilityFormView.as_view(), name='form-post'),
)
