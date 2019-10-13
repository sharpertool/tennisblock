from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/chat/<str:room_name>/', consumers.ChatConsumer),
    path(r'ws/mixer/', consumers.MixerConsumer),
    path(r'ws/schedule/<str:date>/', consumers.ProjectConsumer),
]