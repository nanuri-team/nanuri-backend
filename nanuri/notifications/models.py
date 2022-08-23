from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from nanuri.aws.sns import sns


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
    opt_in = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_device_token = self.device_token

    def save(self, *args, **kwargs):
        if self.device_token != self.previous_device_token:
            sns.delete_endpoint_by_device_token(self.previous_device_token)
            self.previous_device_token = self.device_token
        self.endpoint_arn = sns.create_platform_endpoint(self.device_token)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        sns.delete_endpoint_by_device_token(self.device_token)
        super().delete(*args, **kwargs)


class Subscription(models.Model):
    class Topic(models.TextChoices):
        TO_ALL = "TO_ALL", _("공지사항")
        TO_POST_WRITER = "TO_POST_WRITER", _("공동구매 진행자에게 보내는 푸시 알림")
        TO_POST_PARTICIPANTS = "TO_POST_WRITERS", _("공동구매 참여자에게 보내는 푸시 알림")
        TO_CHAT_ROOM = "TO_CHAT_ROOM", _("채팅방 참가자에게 보내는 푸시 알림")

    uuid = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid4,
        editable=False,
    )
    device = models.ForeignKey("Device", on_delete=models.CASCADE)
    topic = models.CharField(
        max_length=255,
        choices=Topic.choices,
        null=True,
        default=None,
    )
    group_code = models.CharField(max_length=255, null=True, blank=True)
    opt_in = models.BooleanField(default=True)
    subscription_arn = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.subscription_arn is not None:
            sns.unsubscribe(self.subscription_arn)
        if self.opt_in is False:
            self.subscription_arn = None
        else:
            self.subscription_arn = sns.subscribe(
                self.topic,
                self.device.endpoint_arn,
                self.group_code,
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.subscription_arn is not None:
            sns.unsubscribe(self.subscription_arn)
        super().delete(*args, **kwargs)

    class Meta:
        unique_together = [["device", "topic", "group_code"]]
