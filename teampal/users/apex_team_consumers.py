# users/apex_team_consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Apex_Team
import logging
from django.core.serializers.json import DjangoJSONEncoder


logger = logging.getLogger(__name__)

class Apex_TeamSearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "apex_team_search"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        teams = await self.get_teams()
        await self.send(text_data=json.dumps({"type": "all_teams", "teams": teams}))

    @database_sync_to_async
    def get_teams(self):
        return list(Apex_Team.objects.values('name', 'description', 'game', 'members_needed', 'contact', 'creator'))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        logger.info(f"Received data from client: {text_data}")

        if text_data_json.get("type") == "fetch_teams":
            teams = await self.get_teams()
            await self.send(text_data=json.dumps({"type": "all_teams", "teams": teams}))
            print(f"fetched")
        elif text_data_json.get("type") == "cancel_team":
            team_name = text_data_json.get("name", "")
            if not team_name:
                logger.error('Received incomplete data for cancel.')
                return
            await self.cancel_team(team_name)
        else:
            team_name = text_data_json.get("name", "")
            description = text_data_json.get("description", "")
            game = text_data_json.get("game", "")
            members_needed = text_data_json.get("members_needed", 0)
            contact = text_data_json.get("contact", "")
            creator = text_data_json.get("creator", "")


            if not all([team_name, description, game, members_needed, contact, creator]):
                logger.error('Received incomplete data.')
                return

            await self.save_team(team_name, description, game, members_needed, contact, creator)
            await self.channel_layer.group_send(
                self.room_group_name,
               {"type": "team.message", "team": {
                    "name": team_name, "description": description, "game": game,
                 "members_needed": members_needed, "contact": contact, "creator": creator
                }}
        )


    @database_sync_to_async
    def save_team(self, name, description, game, members_needed, contact, creator):
        try:
            team = Apex_Team.objects.create(name=name, description=description, game=game, members_needed=members_needed, contact=contact, creator=creator)
            print(f"Team created: {team}")
        except Exception as e:
            logger.error(f"An error occurred while saving the team: {e}")
    @database_sync_to_async
    def cancel_team(self, team_name):
        try:
            team = Apex_Team.objects.get(name=team_name)
            team.delete()
            logger.info(f"Team {team_name} cancelled successfully.")
        except Apex_Team.DoesNotExist:
            logger.error(f"Team with name {team_name} does not exist.")
        except Exception as e:
            logger.error(f"Error when trying to cancel team {team_name}: {e}")


    async def team_message(self, event):
        team_info = event['team']
        await self.send(text_data=json.dumps({
            "type": "team.message",
            "team": {
                "name": team_info["name"],
                "description": team_info["description"],
                "game": team_info["game"],
                "members_needed": team_info["members_needed"],
                "contact": team_info["contact"],
                "creator": team_info["creator"]
            }
        }))