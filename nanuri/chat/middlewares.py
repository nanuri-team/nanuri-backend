from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(token_key: str):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return None


class QueryTokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["user"] = None
        params = parse_qs(scope["query_string"])
        if b"token" in params.keys():
            token_key = params[b"token"][0].decode()
            user = await get_user(token_key)
            scope["user"] = user
        return await self.app(scope, receive, send)
