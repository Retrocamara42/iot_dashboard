from django.urls import re_path
from environment_monitor import consumers as consumers_env_mon
from AniM5Stack import consumers as consumers_anim5

websocket_urlpatterns = [
    re_path(r'ws/environment_monitor/(?P<device_name>\w+)/$',  consumers_env_mon.EnvMonitorConsumer.as_asgi()),
    re_path(r'ws/anim5stack/(?P<device_name>\w+)/$',  consumers_anim5.AniM5StackConsumer.as_asgi()),
]
