from blog import consumers

from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^notifications/ws$', consumers.ChatConsumer),
]
