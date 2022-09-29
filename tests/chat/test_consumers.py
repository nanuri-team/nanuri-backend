import base64
import io
import json
from uuid import uuid4

import pytest
from asgiref.sync import sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from faker import Faker
from PIL import Image
from rest_framework.authtoken.models import Token

from nanuri.chat.middlewares import QueryTokenAuthMiddleware
from nanuri.chat.routing import websocket_urlpatterns
from tests.users.factories import UserFactory

TIMEOUT = 30

fake = Faker()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_send_text():
    app = QueryTokenAuthMiddleware(URLRouter(websocket_urlpatterns))
    # FIXME: URL에 하이픈(-)이 포함되면 잘 웹소켓 연결이 실패함
    room_name = str(uuid4().hex)
    url = f"/ws/chat/{room_name}/"

    # 사용자 1: 채팅방 입장
    user1 = await sync_to_async(UserFactory.create)()
    token1 = await sync_to_async(Token.objects.create)(user=user1)
    ws1 = WebsocketCommunicator(app, f"{url}?token={token1.key}")
    connected, _ = await ws1.connect(timeout=TIMEOUT)
    assert connected

    # 사용자 2: 채팅방 입장
    user2 = await sync_to_async(UserFactory.create)()
    token2 = await sync_to_async(Token.objects.create)(user=user2)
    ws2 = WebsocketCommunicator(app, f"{url}?token={token2.key}")
    connected, _ = await ws2.connect(timeout=TIMEOUT)
    assert connected

    # 사용자 1: 메시지 전달 (broadcast)
    text = await sync_to_async(fake.sentence)()
    await ws1.send_to(
        text_data=json.dumps(
            {
                "type": "send_message",
                "message": text,
                "format": "plain/text",
            }
        )
    )

    # 사용자 1: 메시지 수신
    response = await ws1.receive_from(timeout=TIMEOUT)
    message = await sync_to_async(json.loads)(response)
    assert message["format"] == "plain/text"
    assert message["message"] == text
    assert message["sender"] == user1.email
    assert "created_at" in message.keys()

    # 사용자 2: 메시지 수신
    response = await ws2.receive_from(timeout=TIMEOUT)
    message = await sync_to_async(json.loads)(response)
    assert message["format"] == "plain/text"
    assert message["message"] == text
    assert message["sender"] == user1.email
    assert "created_at" in message.keys()

    # 웹소켓 연결 해제
    await ws1.disconnect()
    await ws2.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_send_image():
    app = QueryTokenAuthMiddleware(URLRouter(websocket_urlpatterns))
    room_name = str(uuid4().hex)
    url = f"/ws/chat/{room_name}/"

    # 사용자 1: 채팅방 입장
    user1 = await sync_to_async(UserFactory.create)()
    token1 = await sync_to_async(Token.objects.create)(user=user1)
    ws1 = WebsocketCommunicator(app, f"{url}?token={token1.key}")
    connected, _ = await ws1.connect(timeout=TIMEOUT)
    assert connected

    # 사용자 2: 채팅방 입장
    user2 = await sync_to_async(UserFactory.create)()
    token2 = await sync_to_async(Token.objects.create)(user=user2)
    ws2 = WebsocketCommunicator(app, f"{url}?token={token2.key}")
    connected, _ = await ws2.connect(timeout=TIMEOUT)
    assert connected

    # 사용자 1: 이미지 전달 (broadcast)
    image = Image.new(mode="RGB", size=(8, 8))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_b64_encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    await ws1.send_to(
        text_data=json.dumps(
            {
                "type": "send_message",
                "message": image_b64_encoded,
                "format": "image/jpeg",
            }
        )
    )

    # 사용자 1: 이미지 수신
    response = await ws1.receive_from(timeout=TIMEOUT)
    message = json.loads(response)
    assert message["format"] == "image/jpeg"
    assert message["message"] == image_b64_encoded
    assert message["sender"] == user1.email
    assert message["created_at"]

    # 사용자 2: 이미지 수신
    response = await ws2.receive_from(timeout=TIMEOUT)
    message = json.loads(response)
    assert message["format"] == "image/jpeg"
    assert message["message"] == image_b64_encoded
    assert message["sender"] == user1.email
    assert "created_at" in message.keys()

    # 웹소켓 연결 해제
    await ws1.disconnect()
    await ws2.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_load_messages():
    app = QueryTokenAuthMiddleware(URLRouter(websocket_urlpatterns))
    room_name = str(uuid4().hex)
    url = f"/ws/chat/{room_name}/"

    # 사용자 1: 채팅방 입장
    user1 = await sync_to_async(UserFactory.create)()
    token1 = await sync_to_async(Token.objects.create)(user=user1)
    ws = WebsocketCommunicator(app, f"{url}?token={token1.key}")
    connected, _ = await ws.connect(timeout=TIMEOUT)
    assert connected

    # 사용자 1: 이전 채팅 기록 불러오기 요청
    await ws.send_to(text_data=json.dumps({"type": "load_messages"}))

    # 사용자 1: 이전 채팅 기록 수신
    response = await ws.receive_from(timeout=TIMEOUT)
    message = json.loads(response)
    for item in message["message"]:
        assert "channel_id" in item.keys()
        assert "message_id" in item.keys()
        assert "message" in item.keys()
        assert "format" in item.keys()
        assert "message_from" in item.keys()
        assert "message_to" in item.keys()
        assert "created_at" in item.keys()

    # 웹소켓 연결 해제
    await ws.disconnect()
