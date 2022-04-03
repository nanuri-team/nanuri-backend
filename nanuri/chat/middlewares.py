from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(token_key: str):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class QueryTokenAuthMiddleware:
    """
    쿼리 문자열에서 토큰 값을 가지고 와서 인증을 수행하는 커스텀 미들웨어

    https://channels.readthedocs.io/en/stable/topics/authentication.html#custom-authentication
    """

    def __init__(self, app):
        # 우리가 전달했던 ASGI 애플리케이션 저장
        self.app = app

    async def __call__(self, scope, receive, send):
        scope['user'] = AnonymousUser()
        params = parse_qs(scope['query_string'])
        if b'token' in params.keys():
            token_key = params[b'token'][0].decode()
            user = await get_user(token_key)
            scope['user'] = user
        return await self.app(scope, receive, send)
