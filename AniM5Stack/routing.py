from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/anim5stack/(?P<device_name>\w+)/$',  consumers.AniM5StackConsumer.as_asgi()),
]
