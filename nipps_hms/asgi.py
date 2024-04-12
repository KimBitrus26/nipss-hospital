
import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from core.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nipps_hms.settings')

django.setup()

from .custom_middleware import QueryAuthMiddleware


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        QueryAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
        ),
})
