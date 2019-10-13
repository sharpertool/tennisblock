import json
import logging
from json import JSONDecodeError

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class MixerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.mixer_channel = 'tennis_mixer_group'

        # Join project notification channel
        await self.channel_layer.group_add(
            self.mixer_channel,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave notification channel
        await self.channel_layer.group_discard(
            self.mixer_channel,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Not sure what client will send me regarding the
        channel. Ignore for now.
        :param text_data:
        :return:
        """
        pass

    async def mixer_event(self, event):
        """
        Initiated from a backend action.

        Broadcast an event to all clients
        Event action maps to a redux action name
        Payload is the data for the action
        :param event:
        :return:
        """

        logger.debug(f"project.event Event:{event}")

        await self.send(text_data=json.dumps({
            'action': event.get("action", 'unknownAction'),
            'payload': event.get("payload", {})
        }))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    # Broadcast to group that a client has joined
    # "ed has joined the channel" -- etc.
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
        except JSONDecodeError as e:
            message = text_data

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class ScheduleConsumer(AsyncWebsocketConsumer):

    @staticmethod
    def calc_group_name(date):
        return f"schedule_{date}"

    async def connect(self):
        date = self.scope['url_route']['kwargs']['date']
        self.notify_group = self.calc_group_name(date)

        logger.debug(f"Connection on {date} to {self.channel_name}")
        logger.debug(f"Notify Group: {self.notify_group}")

        # Join room group
        await self.channel_layer.group_add(
            self.notify_group,
            self.channel_name
        )

        await self.accept()

        await self.onConnect()


    async def disconnect(self, close_code):
        # Leave room group
        logger.debug(f"Closing the channel with code {close_code}")
        await self.channel_layer.group_discard(
            self.notify_group,
            self.channel_name
        )

    async def onConnect(self):
        """ Send a welcome message to new client """

        # await self.send(text_data=json.dumps({
        #     'action': 'actionGroupConnected',
        #     'payload': {'last_event': 'yesterday'}
        # }))

    async def receive(self, text_data):
        """
        Process message received from wss client

        There are not a lot of reason for the client to
        talk to the server, but perhaps they could  ask
        a question??

        :param text_data:
        :return:
        """

        print(f"Incoming message from {self.channel_name}: {text_data}")

        try:
            logger.debug(f"parsing {text_data}")
            data = json.loads(text_data)

            action = data.get('action')

            if action == 'refreshOldComments':
                await self.send(text_data=json.dumps({
                    'action': 'refreshOldComments',
                    'payload': {'last_update': '5 minutes ago'}
                }))
        except JSONDecodeError as e:
            pass

    async def schedule_event(self, event):
        """
        Broadcast an event to all clients
        Event action maps to a redux action name
        Payload is the data for the action
        :param event:
        :return:
        """

        logger.debug(f"comment.event Event:{event}")

        await self.send(text_data=json.dumps({
            'action': event.get("action", 'unknownAction'),
            'payload': event.get("payload", {})
        }))

