import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import tasks.routing
import config_search.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SysOpsSuite.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                tasks.routing.websocket_urlpatterns
                + config_search.routing.websocket_urlpatterns
            )
        ),
    }
)
