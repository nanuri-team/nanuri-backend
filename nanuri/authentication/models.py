from django.conf import settings
from django.db import models


class KakaoAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    kakao_id = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        default=None,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
