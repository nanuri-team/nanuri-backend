from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Device(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_token = models.TextField(null=True, blank=True)
    endpoint_arn = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    class Topic(models.TextChoices):
        CHAT_MESSAGE_NOTIFICATIONS = "chat_message_notification", _("채팅 메시지 알림")
        COMMENT_NOTIFICATIONS = "comment_notification", _("댓글 알림")

    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False,
    )
    device = models.ForeignKey("Device", on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
    topic = models.CharField(
        max_length=255,
        choices=Topic.choices,
        null=True,
        blank=False,
    )
    subscription_arn = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["device", "post", "topic"]]
