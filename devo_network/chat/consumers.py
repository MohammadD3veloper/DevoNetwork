import json

from django.db.models.query import QuerySet
from django.forms import model_to_dict

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async

from .selectors import Selector
from .services import Service


class SocialNetworkConsumer(AsyncWebsocketConsumer):
    """ Social Network websocket server """

    async def connect(self):
        """ Initializing connection for websocket requests """
        self.room_name = f"chat_{self.scope['url_route']['kwargs']['id']}"
        self.user = self.scope['user']
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        """ Recieve data from websocket connections """
        content = json.loads(text_data)
        data_types = {
            'chat_list': self.get_chat_list,
            'send_chat': self.send_chat,
            'update_chat': self.update_chat,
            'delete_chat': self.delete_chat,
            'join_group': self.join_group,
            'leave_group': self.leave_group,
            'send_notif': self.send_notif,
        }
        input_type = content['type']
        if input_type in data_types.keys():
            output = await data_types[input_type](content)
            serialized_output = await self.serialize_object(output)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "message": serialized_output
                }
            )


    async def disconnect(self, code):
        """ Disconnect websocket connections """
        raise StopConsumer("Chat disconnected")


    @sync_to_async
    def serialize_object(self, object):
        """ Serializing given object """
        if isinstance(object, QuerySet):
            serialized_object = json.dumps(list(object))
        else:
            serialized_object = json.dumps(model_to_dict(object))
        return serialized_object


    async def chat_message(self, content):
        """ converting datas to a json """
        await self.send(json.dumps({
            "message": content["message"]
        }))


    async def get_chat_list(self, content):
        return await Selector.get_user_groups(self.user)


    async def send_chat(self, content):
        file = content['file_obj']
        group = content['group']
        content = content['content']
        to_user = content['to_user']
        replied_to_message = content['replied_to']
        return await Service.create_message(file, group,
                        content, self.user, to_user, replied_to_message)


    async def update_chat(self, content):
        content = content['content']
        message_id = content['message_id']
        return await Service.update_message(message_id, content)


    async def delete_chat(self, content):
        message_id = content['message_id']
        return await Service.delete_message(message_id)


    async def send_notif(self, content):
        message_id = content['message_id']
        user = self.user
        to_user = content['to_user']
        content = content['content']
        return await Service.create_notification(message_id, user, to_user, content)


    async def join_group(self, content):
        group = content['group']
        user = self.user
        return await Service.join_group(group, user)


    async def leave_group(self, content):
        group = content['group']
        user = self.user
        return await Service.leave_group(group, user)
