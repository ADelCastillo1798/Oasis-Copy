import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from pages.models import Message, Conversation


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = 'chat_%s' % self.conversation_id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']
        conversation_id = text_data_json['conversation_id']
        sender = text_data_json['sentby_id']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'conversation_id': conversation_id,
                'sentby_id': sender,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print(event)
        message = event['message']
        conversation_id = event['conversation_id']
        sender = event['sentby_id']
        #save message to database?
        await self.save_message(message, conversation_id)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sentby_id': sender
        }))


    @database_sync_to_async
    def save_message(self, message, conversation_id):
        current_conversation=Conversation.objects.get(id=conversation_id)
        Message.objects.create(message=message, sentby=self.scope["user"], conversation=current_conversation)
