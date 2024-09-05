from django.urls import re_path
from .consumers import TriggerConsumer

websocket_urlpatterns = [
    re_path(r"ws/trigger-socket-server/", TriggerConsumer.as_asgi()),
]
