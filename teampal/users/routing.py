from django.urls import re_path
from .consumers import ChatConsumer
from .team_consumers import TeamSearchConsumer
from .trade_consumers import TradeConsumer
from .tour_consumers import TourConsumer
from .apex_team_consumers import Apex_TeamSearchConsumer



websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/team_search/$", TeamSearchConsumer.as_asgi()),
    re_path(r"ws/trade_search/$", TradeConsumer.as_asgi()),
    re_path(r"ws/tournaments/$", TourConsumer.as_asgi()),
    re_path(r"ws/apex_team_search/$", Apex_TeamSearchConsumer.as_asgi()),
]
