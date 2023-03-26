from urllib.parse import parse_qs

from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async

from devo_network.authentication.selectors import Selector


@database_sync_to_async
def get_user(pk):
    """ get query to db for getting user object """
    return Selector.get_user_info(pk)



class TokenAuthMiddleWare:
    """ get token of websocket connection """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"]
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        token = query_dict["token"][0]
        scope["user"] = await get_user(AccessToken(token)['user_id'])
        return await self.app(scope, receive, send)
