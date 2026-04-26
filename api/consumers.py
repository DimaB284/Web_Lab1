import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'game_room'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        coordinate = text_data_json['coordinate']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'fire_shot',
                'coordinate': coordinate
            }
        )

    async def fire_shot(self, event):
        coordinate = event['coordinate']
        await self.send(text_data=json.dumps({
            'coordinate': coordinate,
            'message': f'Shot to {coordinate}!'
        }))