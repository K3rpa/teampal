# users/consumers.py
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection before sending messages
        await self.accept()

        # Load and send room's history messages to user
        last_messages = await self.get_last_messages(self.room_name)
        for message_data in last_messages:
            await self.send(text_data=json.dumps({
                "message": message_data['content'],
                "author": message_data['author_username'] if message_data['author_username'] else "undefine",
                "timestamp": message_data['timestamp']
            }))

    async def get_last_messages(self, room_name):
        @database_sync_to_async
        def get_messages():
            messages = Message.objects.filter(room_name=room_name).order_by('timestamp')[:10]
            return [{
                'content': message.content,
                'author_username': message.author.username if message.author else None,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            } for message in messages]

        return await get_messages()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Get user information
        user = self.scope['user']
        username = user.username if user.is_authenticated else "undefine"

        # Save message to database
        await self.save_message(user, message, self.room_name)

        # Send message to room group with author information
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "author": username,
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        author = event.get("author", "undefine")
        timestamp = event.get("timestamp", str(datetime.now()))


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "author": author,
            "timestamp": timestamp,
        }))

    @database_sync_to_async
    def save_message(self, user, message, room_name):
        User = get_user_model()
        try:
            author_user = User.objects.get(username=user.username) if user.is_authenticated else None
            Message.objects.create(author=author_user, content=message, room_name=room_name)
        except ObjectDoesNotExist:
            print(f"Failed to find user with username {user.username}")
        except Exception as e:
             print(f"An error occurred: {e}")