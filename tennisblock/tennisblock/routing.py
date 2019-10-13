from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import tennis_channels.routing

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_config")

application = ProtocolTypeRouter({
    # Empty, with defaults for http->django
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                tennis_channels.routing.websocket_urlpatterns
            )
        )
    )
})
