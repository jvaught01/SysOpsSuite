from django.urls import re_path
from .consumers import SearchConsumer

websocket_urlpatterns = [
    re_path(r"ws/search-socket-server/", SearchConsumer.as_asgi()),
]
