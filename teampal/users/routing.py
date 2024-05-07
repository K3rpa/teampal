from django.urls import re_path
from .consumers import ChatConsumer
from .team_consumers import TeamSearchConsumer
from .trade_consumers import TradeConsumer
from .tour_consumers import TourConsumer
from .apex_team_consumers import Apex_TeamSearchConsumer
from .cs2_team_consumers import cs2_TeamSearchConsumer
from .lol_team_consumers import lol_TeamSearchConsumer
from .valorant_team_consumers import valorant_TeamSearchConsumer




websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/team_search/$", TeamSearchConsumer.as_asgi()),
    re_path(r"ws/trade_search/$", TradeConsumer.as_asgi()),
    re_path(r"ws/tournaments/$", TourConsumer.as_asgi()),
    re_path(r"ws/apex_team_search/$", Apex_TeamSearchConsumer.as_asgi()),
    re_path(r"ws/cs2_team_search/$", cs2_TeamSearchConsumer.as_asgi()),
    re_path(r"ws/lol_team_search/$", lol_TeamSearchConsumer.as_asgi()),
    re_path(r"ws/valorant_team_search/$", valorant_TeamSearchConsumer.as_asgi()),

]
