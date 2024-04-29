from django.urls import re_path
from .consumers import ChatConsumer
from .team_consumers import TeamSearchConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/team_search/$", TeamSearchConsumer.as_asgi()),
]
