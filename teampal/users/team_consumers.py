# users/team_consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Team
import logging

logger = logging.getLogger(__name__)

class TeamSearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "team_search"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        teams = await self.get_teams()
        await self.send(text_data=json.dumps({"type": "all_teams", "teams": teams}))

    @database_sync_to_async
    def get_teams(self):
        return list(Team.objects.values('name', 'description', 'game', 'members_needed', 'contact'))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        team_name = text_data_json.get("name", "")
        description = text_data_json.get("description", "")
        game = text_data_json.get("game", "")
        members_needed = text_data_json.get("members_needed", 0)
        contact = text_data_json.get("contact", "")

        if not all([team_name, description, game, members_needed, contact]):
            logger.error('Received incomplete data.')
            return

        await self.save_team(team_name, description, game, members_needed, contact)
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "team.message", "team": {
                "name": team_name, "description": description, "game": game,
                "members_needed": members_needed, "contact": contact
            }}
        )

    @database_sync_to_async
    def save_team(self, name, description, game, members_needed, contact):
        try:
            Team.objects.create(name=name, description=description, game=game, members_needed=members_needed, contact=contact)
        except Exception as e:
            logger.error(f"An error occurred while saving the team: {e}")

    async def team_message(self, event):
        await self.send(text_data=json.dumps({
            "name": event["name"],
            "description": event["description"],
            "game": event["game"],
            "members_needed": event["members_needed"],
            "contact": event["contact"]
        }))
