import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from nanuri.aws.dynamodb import group_message_table

logger = logging.getLogger(__name__)


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]

        if self.user is None:
            logger.info("인증되지 않은 유저가 '%s' 방에 접속하려고 시도했으며 이를 거절했습니다", self.room_name)
            return await self.close()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        logger.info("'%s'가 '%s' 방에 접속했습니다.", self.user.email, self.room_name)
        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        if self.user is not None:
            logger.info("'%s'가 '%s' 방을 나갔습니다.", self.user.email, self.room_name)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_type = text_data_json["type"]

        # 클라이언트가 채팅 방에 메시지를 보내고 싶어 하는 경우
        if message_type == "send_message":
            message_format = text_data_json["format"]
            message = text_data_json["message"]

            row = group_message_table.insert_row(
                channel_id=self.room_name,
                message_to=self.room_group_name,
                message_from=self.user.email,
                message=message,
                message_format=message_format,
            )
            logger.info(
                "'%s'가 '%s' 그룹에게 메시지를 전달했습니다: '%s'",
                self.user.email,
                self.room_group_name,
                message,
            )

            # 채팅방 내 모든 사람 (그룹)에게 메시지 전송하기 위해 그룹 센드
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send_message",
                    "format": row["format"],
                    "message": row["message"],
                    "sender": row["message_from"],
                    "created_at": row["created_at"],
                },
            )

        # 클라이언트가 이전 채팅 기록을 불러오고 싶어 하는 경우
        elif message_type == "load_messages":
            await self.channel_layer.send(
                self.channel_name,
                {
                    "type": "load_messages",
                    "channel_id": self.room_name,
                },
            )

    # Receive message from room group
    async def send_message(self, event):
        message = event["message"]
        message_format = event["format"]
        sender = event["sender"]
        created_at = event["created_at"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "format": message_format,
                    "sender": sender,
                    "created_at": created_at,
                }
            )
        )

    async def load_messages(self, event):
        channel_id = event["channel_id"]
        rows = [
            {
                "channel_id": r["channel_id"],
                "message_id": float(r["message_id"]),
                "format": r.get("format", "plain/text"),
                "message": r["message"],
                "message_from": r["message_from"],
                "message_to": r["message_to"],
                "created_at": r["created_at"],
            }
            for r in group_message_table.query_by_channel_id(channel_id)
        ]
        rows.sort(key=lambda x: x["message_id"])
        logger.info(
            "'%s'가 '%s' 방으로부터 %s개의 채팅 기록을 불러왔습니다.",
            self.user.email,
            self.room_name,
            len(rows),
        )
        await self.send(text_data=json.dumps({"message": rows}))
