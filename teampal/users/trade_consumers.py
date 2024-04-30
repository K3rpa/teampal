# users/trade_consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
import json
import logging
from .models import Trade

logger = logging.getLogger(__name__)

class TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "trade_search"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        trades = await self.get_trades()
        await self.send(text_data=json.dumps({"type": "all_trades", "trades": trades}))

    @database_sync_to_async
    def get_trades(self):
        return list(Trade.objects.values('game_name', 'item_name', 'description', 'status', 'quantity', 'expected_price', 'current_offer', 'current_quantity', 'creator'))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get("type") == "fetch_trades":
            trades = await self.get_trades()
            await self.send(text_data=json.dumps({"type": "all_trades", "trades": trades}))
        else:
            game_name = text_data_json.get("game_name", "")
            item_name = text_data_json.get("item_name", "")
            description = text_data_json.get("description", "")
            status = text_data_json.get("status", "")
            quantity = text_data_json.get("quantity", 0)
            expected_price = text_data_json.get("expected_price", 0.0)
            current_offer = text_data_json.get("current_offer", 0.0)
            current_quantity = text_data_json.get("current_quantity", 0)
            creator_email = text_data_json.get("creator", "")

            if not all([game_name, item_name, description, status, quantity, expected_price, creator]):
                logger.error('Received incomplete data.')
                return

            await self.save_trade(game_name, item_name, description, status, quantity, expected_price, current_offer, current_quantity, creator_email)
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "trade.message", "trade": {
                    "game_name": game_name,
                    "item_name": item_name,
                    "description": description,
                    "status": status,
                    "quantity": quantity,
                    "expected_price": expected_price,
                    "current_offer": current_offer,
                    "current_quantity": current_quantity,
                    "creator": creator_email
                }}
            )

    @database_sync_to_async
    def save_trade(self, game_name, item_name, description, status, quantity, expected_price, current_offer, current_quantity, creator):
        try:
            creator = User.objects.get(email=creator_email)

            trade, created = Trade.objects.update_or_create(
                game_name=game_name, item_name=item_name, defaults={
                    'description': description,
                    'status': status,
                    'quantity': quantity,
                    'expected_price': expected_price,
                    'current_offer': current_offer,
                    'current_quantity': current_quantity,
                    'creator': creator
                }
            )
            if created:
                logger.info(f"Trade created: {trade}")
            else:
                logger.info(f"Trade updated: {trade}")
        except User.DoesNotExist:
            logger.error(f"No user found with email {creator_email}")
        except Exception as e:
            logger.error(f"An error occurred while saving the trade: {e}")

    async def trade_message(self, event):
        trade_info = event['trade']
        await self.send(text_data=json.dumps({
            "type": "trade.message",
            "trade": trade_info
        }))
