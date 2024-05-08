# users/apex_trade_consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
import json
import logging
from .models import apex_Trade, apex_Offer
logger = logging.getLogger(__name__)
class apex_TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "apex_trade_search"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        trades = await self.get_trades()
        await self.send(text_data=json.dumps({"type": "all_trades", "trades": trades}))
    @database_sync_to_async
    def get_trades(self):
        return list(apex_Trade.objects.values(
            'id', 'game_name', 'item_name', 'description', 'status', 
            'quantity', 'expected_price', 'current_offer', 'current_quantity', 'creator__email'
        ))
    @database_sync_to_async
    def get_trade_offers(self, trade_id):
        offers = apex_Offer.objects.filter(trade_id=trade_id).order_by('-created_at').values(
            'user__username', 'offer_price', 'offer_quantity'
        )
        return [{
            'user_username': offer['user__username'],
            'offer_price': offer['offer_price'],
            'offer_quantity': offer['offer_quantity']
        } for offer in offers]
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    async def receive(self, text_data):
        logger.info(f"Received message: {text_data}")
        text_data_json = json.loads(text_data)
        User = get_user_model()
        if text_data_json.get("type") == "fetch_trades":
            trades = await self.get_trades()
            await self.send(text_data=json.dumps({"type": "all_trades", "trades": trades}))
        elif text_data_json.get("type") == "create_trade":
            creator_email = text_data_json['creator']
            await self.create_trade(text_data_json, creator_email)
        elif text_data_json.get("type") == "make_offer":
            offerer_email = text_data_json['user_email']
            await self.create_or_update_offer(
                item_name=text_data_json["item_name"],
                email=offerer_email,
                offer_price=text_data_json['offer_price'],
                offer_quantity=text_data_json['offer_quantity']
            )
        elif text_data_json.get("type") == "cancel_trade":
            trade_id = text_data_json.get("id", "")
            await self.cancel_trade(trade_id)
        elif text_data_json.get("type") == "fetch_offers":
            trade_id = text_data_json.get("trade_id", "")
            offers = await self.get_trade_offers(trade_id)
            await self.send(text_data=json.dumps({"type": "trade_offers", "offers": offers}))
    @database_sync_to_async
    def cancel_trade(self, trade_id):
        try:
            trade = apex_Trade.objects.get(id=trade_id)
            trade.delete()
            logger.info(f"Trade {trade_id} cancelled successfully.")
        except apex_Trade.DoesNotExist:
            logger.error(f"Trade with id {trade_id} does not exist.")
        except Exception as e:
            logger.error(f"Error when trying to cancel trade {trade_id}: {e}")




    async def create_or_update_offer(self, item_name, email, offer_price, offer_quantity):
        User = get_user_model()
        user = await database_sync_to_async(User.objects.get)(email=email)
        try:
            trade = await database_sync_to_async(apex_Trade.objects.get)(item_name=item_name)
            offer, created = await database_sync_to_async(apex_Offer.objects.update_or_create)(
                trade=trade,
                user=user,
                defaults={'offer_price': offer_price, 'offer_quantity': offer_quantity}
            )
            logger.info(f"Processing new offer for trade {trade.id}: {offer_price} offered by {email}")
            if trade.status == 'WTB' and (trade.current_offer is None or offer_price < trade.current_offer):
                trade.current_offer = offer_price
                trade.current_quantity = offer_quantity
            elif trade.status == 'WTS' and (trade.current_offer is None or offer_price > trade.current_offer):
                trade.current_offer = offer_price
                trade.current_quantity = offer_quantity
            ##await database_sync_to_async(trade.save)()
            await self.update_trade_current_offer(trade, offer_price, offer_quantity)
        except apex_Trade.DoesNotExist:
            logger.error(f"No trade found with item_name {item_name}.")




    async def update_trade_current_offer(self, trade, new_offer_price, new_offer_quantity):
        if trade.status == 'WTB':
            if trade.current_offer is None or new_offer_price < trade.current_offer:
                trade.current_offer = new_offer_price
                trade.current_quantity = new_offer_quantity

        elif trade.status == 'WTS':
            if trade.current_offer is None or new_offer_price > trade.current_offer:
                trade.current_offer = new_offer_price
                trade.current_quantity = new_offer_quantity

        await database_sync_to_async(trade.save)()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "trade.update",
                "trade": {
                    'id': trade.id,
                    'current_offer': trade.current_offer,
                    'current_quantity': trade.current_quantity,
                }
            }
        )
    
    async def create_trade(self, data, creator_email):
        User = get_user_model()
        creator = await database_sync_to_async(User.objects.get)(email=creator_email)
        trade = await database_sync_to_async(apex_Trade.objects.create)(
            game_name=data['game_name'],
            item_name=data['item_name'],
            description=data['description'],
            status=data['status'],
            quantity=data['quantity'],
            expected_price=data['expected_price'],
            current_offer=0,
            current_quantity=0,
            creator=creator
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "trade.message",
                "trade": {
                    'id': trade.id,
                    'game_name': trade.game_name,
                    'item_name': trade.item_name,
                    'description': trade.description,
                    'status': trade.status,
                    'quantity': trade.quantity,
                    'expected_price': trade.expected_price,
                    'current_offer': trade.current_offer,
                    'current_quantity': trade.current_quantity,
                    'creator__email': creator.email
                }
            }
        )
    async def trade_message(self, event):
        trade_info = event['trade']
        await self.send(text_data=json.dumps({
            'type': 'trade.message',
            'trade': trade_info
        }))

    async def trade_update(self, event):
        trade_info = event['trade']
        await self.send(text_data=json.dumps({
            'type': 'trade.update',
            'trade': trade_info
        }))
