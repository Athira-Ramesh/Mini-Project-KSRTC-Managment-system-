from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from store import consumers

websocket_urlpatterns = [
    path('chat/<room_id>/', consumers.ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        websocket_urlpatterns
    ),
})