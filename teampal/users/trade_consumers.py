# users/trade_consumers.py

# trade_consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
import json
import logging
from .models import Trade, Offer

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
        return list(Trade.objects.values('id', 'game_name', 'item_name', 'description', 'status', 'quantity', 'expected_price', 'current_offer', 'current_quantity', 'creator__email'))

    @database_sync_to_async
    def get_trade_offers(self, trade_id):
        offers = Offer.objects.filter(trade_id=trade_id).order_by('-created_at').values('user__username', 'offer_price', 'offer_quantity', 'created_at')
        return list(offers)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get("type") == "fetch_trades":
            trades = await self.get_trades()
            await self.send(text_data=json.dumps({"type": "all_trades", "trades": trades}))
        elif text_data_json.get("type") == "cancel_trade":
            trade_id = text_data_json.get("id", "")
            await self.cancel_trade(trade_id)
        elif text_data_json.get("type") == "fetch_offers":
            trade_id = text_data_json.get("trade_id", "")
            offers = await self.get_trade_offers(trade_id)
            await self.send(text_data=json.dumps({"type": "trade_offers", "offers": offers}))
        else:
            await self.process_trade_data(text_data_json)

    @database_sync_to_async
    def cancel_trade(self, trade_id):
        try:
            trade = Trade.objects.get(id=trade_id)
            trade.delete()
            logger.info(f"Trade {trade_id} cancelled successfully.")
        except Trade.DoesNotExist:
            logger.error(f"Trade with id {trade_id} does not exist.")
        except Exception as e:
            logger.error(f"Error when trying to cancel trade {trade_id}: {e}")

    @database_sync_to_async
    def process_trade_data(self, data):
        User = get_user_model()
        try:
            creator = User.objects.get(email=data['creator'])
            defaults = {
                'description': data['description'],
                'status': data['status'],
                'quantity': data['quantity'],
                'expected_price': data['expected_price'],
                'current_offer': data['expected_price'],
                'current_quantity': 0,
                'creator': creator
            }
            trade, created = Trade.objects.update_or_create(game_name=data['game_name'], item_name=data['item_name'], defaults=defaults)
            if created:
                logger.info(f"Trade created: {trade}")
            else:
                logger.info(f"Trade updated: {trade}")
        except User.DoesNotExist:
            logger.error(f"No user found with email {data['creator']}")
        except Exception as e:
            logger.error(f"An error occurred while processing trade data: {e}")

    async def trade_message(self, event):
        trade_info = event['trade']
        await self.send(text_data=json.dumps({
            "type": "trade.message",
            "trade": trade_info
        }))
        logger.info(f"Sending trade info to client: {trade_info}")  # Debugging log

