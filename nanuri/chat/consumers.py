import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'room_name': self.room_name,
                'sender': self.user.email,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        new_message = await self.create_message(message, self.room_name, self.user)

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    'message': new_message.message,
                    'room_name': new_message.room_name,
                    'sender': new_message.sender.email,
                    'sent_at': new_message.sent_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )
        )

    @database_sync_to_async
    def create_message(self, message, room_name, sender):
        new_message = Message.objects.create(
            message=message,
            room_name=room_name,
            sender=sender,
        )
        new_message.save()
        return new_message
