from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/environment_monitor/(?P<device_name>\w+)/$',  consumers.EnvMonitorConsumer.as_asgi()),
]
