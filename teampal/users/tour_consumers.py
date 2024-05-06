# tour_consumers.py
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import TournamentPost
import logging
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F



logger = logging.getLogger(__name__)

class TourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "tournament_search"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(f"WebSocket connected")
        tournaments = await self.get_tournaments()
        await self.send(text_data=json.dumps({"type": "all_tournaments", "tournaments": json.loads(tournaments)}))

    @database_sync_to_async
    def get_tournaments(self):
        User = get_user_model()

        tournaments = TournamentPost.objects.annotate(creator_email=F('creator__email')).values(
        'name', 'game', 'date', 'description', 'team_count', 'prize', 
        'interest_count', 'website', 'contact', 'creator_email')
        return json.dumps(list(tournaments), cls=DjangoJSONEncoder)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info(f"Received data from client: {text_data}")
        text_data_json = json.loads(text_data)
        if text_data_json.get("type") == "fetch_tournaments":
            tournaments = await self.get_tournaments()
            await self.send(text_data=json.dumps({"type": "all_tournaments", "tournaments": tournaments}))
            logger.info('Tournaments fetched successfully.')
        elif text_data_json.get("type") == "create_tournament":
            logger.info("Creating tournament with data: " + str(text_data_json))
            await self.create_tournament(text_data_json)
        elif text_data_json.get("type") == "toggle_interest":
            await self.toggle_interest(text_data_json.get("name"))
        elif text_data_json.get("type") == "cancel_tournament":
            await self.cancel_tournament(text_data_json.get("name"))

    @database_sync_to_async
    def create_tournament(self, data):
        User = get_user_model()
        creator_email = data['creator']
        creator = User.objects.get(email=creator_email)

        try:
            logger.info(f"Attempting to create tournament with data: {data}")
            tournament = TournamentPost.objects.create(
                name=data['name'],
                game=data['game'],
                date=data['date'],
                description=data['description'],
                team_count=data['team_count'],
                prize=data['prize'],
                interest_count=0,
                website=data.get('website', ''),
                contact=data['contact'],
                creator=creator  
            )
            logger.info(f"Tournament created: {tournament}")
        except Exception as e:
            logger.error(f"An error occurred while creating the tournament: {e}")

    @database_sync_to_async
    def cancel_tournament(self, name):
        try:
            tournament = TournamentPost.objects.get(name=name)
            tournament.delete()
            logger.info(f"Tournament {name} cancelled successfully.")
        except TournamentPost.DoesNotExist:
            logger.error(f"Tournament with name {name} does not exist.")
        except Exception as e:
            logger.error(f"Error when trying to cancel tournament {name}: {e}")

    @database_sync_to_async
    def toggle_interest(self, name):
        try:
            tournament = TournamentPost.objects.get(name=name)
            tournament.interest_count = F('interest_count') + 1
            tournament.save()
            logger.info(f"Interest toggled for tournament {name}.")
        except TournamentPost.DoesNotExist:
            logger.error(f"Tournament with name {name} does not exist.")
        except Exception as e:
            logger.error(f"Error when trying to toggle interest for tournament {name}: {e}")

    async def tournament_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "tournament.update",
            "tournament": event['tournament']
        }))

    async def tournament_message(self, event):
        tournament_info = event['tournament']
        await self.send(text_data=json.dumps({
            "type": "tournament.message",
            "tournament": {
                "name": tournament_info["name"],
                "description": tournament_info["description"],
                "game": tournament_info["game"],
                "date": tournament_info["date"],
                "team_count": tournament_info["team_count"],
                "prize": tournament_info["prize"],
                "interest_count": tournament_info["interest_count"],
                "website": tournament_info["website"],
                "contact": tournament_info["contact"],
                "creator": tournament_info["creator"]
            }
        }))

    async def send_tournament_update(self, tournament_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tournament.update',
                'tournament': tournament_data
            }
        )

    async def fetch_tournaments(self):
        tournaments = await database_sync_to_async(self.get_tournaments)()
        await self.send(text_data=json.dumps({
            "type": "all_tournaments",
            "tournaments": json.loads(tournaments)
        }))


