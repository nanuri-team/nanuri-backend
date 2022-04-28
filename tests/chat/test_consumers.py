import json
from datetime import datetime

import pytest
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator

from nanuri.chat.middlewares import QueryTokenAuthMiddleware
from nanuri.chat.routing import websocket_urlpatterns


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_group_chat_consumer(token):
    application = QueryTokenAuthMiddleware(URLRouter(websocket_urlpatterns))

    # 사용자 1: 채팅방 입장
    communicator1 = WebsocketCommunicator(application, f"/ws/chat/test_room/?token={token.key}")
    connected, _ = await communicator1.connect()
    assert connected

    # 사용자 2: 채팅방 입장
    communicator2 = WebsocketCommunicator(application, f"/ws/chat/test_room/?token={token.key}")
    connected, _ = await communicator2.connect()
    assert connected

    # 사용자 1: 메시지 전달 (broadcast)
    await communicator1.send_to(text_data=json.dumps({"type": "send_message", "message": "hello"}))

    # 사용자 1: 메시지 수신
    response = await communicator1.receive_from()
    result = json.loads(response)
    assert result["message"] == "hello"
    assert result["sender"] == token.user.email
    assert datetime.strptime(result["created_at"], "%Y-%m-%d %H:%M:%S")

    # 사용자 2: 메시지 수신
    response = await communicator2.receive_from()
    result = json.loads(response)
    assert result["message"] == "hello"
    assert result["sender"] == token.user.email
    assert datetime.strptime(result["created_at"], "%Y-%m-%d %H:%M:%S")

    # 웹소켓 연결 해제
    await communicator1.disconnect()
    await communicator2.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_load_messages(token):
    application = QueryTokenAuthMiddleware(URLRouter(websocket_urlpatterns))

    # 사용자: 채팅방 입장
    communicator = WebsocketCommunicator(application, f"/ws/chat/test_room/?token={token.key}")
    connected, _ = await communicator.connect()
    assert connected

    # 사용자: 이전 채팅 기록 불러오기 요청
    await communicator.send_to(text_data=json.dumps({"type": "load_messages"}))

    # 사용자: 이전 채팅 기록 수신
    response = await communicator.receive_from()
    result = json.loads(response)
    assert isinstance(result["message"], list)
    for message in result["message"]:
        assert isinstance(message, dict)
        assert message["channel_id"] == "test_room"
        assert "message_id" in message.keys()
        assert "message" in message.keys()
        assert "message_from" in message.keys()
        assert "message_to" in message.keys()
        assert "created_at" in message.keys()

    await communicator.disconnect()
