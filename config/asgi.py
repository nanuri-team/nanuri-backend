"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import nanuri.chat.middlewares
import nanuri.chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': nanuri.chat.middlewares.QueryTokenAuthMiddleware(
            URLRouter(nanuri.chat.routing.websocket_urlpatterns)
        ),
    }
)
