"""
ASGI config for devo_network project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from devo_network.chat.consumers import SocialNetworkConsumer
from devo_network.chat.middlewares import TokenAuthMiddleWare

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.local')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
       TokenAuthMiddleWare(
           URLRouter([
               path("chat/<int:id>/", SocialNetworkConsumer.as_asgi()),
           ])
       )
    )
})
