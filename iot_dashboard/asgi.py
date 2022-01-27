"""
ASGI config for iot_dashboard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iot_dashboard.settings')

from django.core.wsgi import get_wsgi_application
application=get_wsgi_application()

from django.core.asgi import get_asgi_application
asgi_app=get_asgi_application()

import django
import environment_monitor.routing
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            environment_monitor.routing.websocket_urlpatterns
        )
    ),
})
