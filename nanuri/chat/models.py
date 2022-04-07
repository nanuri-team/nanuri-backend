from django.conf import settings
from django.db import models


class Message(models.Model):
    message = models.TextField()
    room_name = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.message
