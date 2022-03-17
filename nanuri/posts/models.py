import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from nanuri.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    uuid = models.UUIDField(
        verbose_name='uuid',
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    unit_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    min_participants = models.PositiveIntegerField()
    max_participants = models.PositiveIntegerField()
    num_participants = models.PositiveIntegerField(default=0)
    product_url = models.URLField()
    trade_type = models.CharField(
        max_length=15,
        choices=(
            ('DIRECT', _('직거래')),
            ('PARCEL', _('택배 거래')),
        ),
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    participants = models.ManyToManyField(User)

    def __str__(self):
        return self.title


class Order(models.Model):
    price = models.PositiveIntegerField()
    status = models.CharField(
        max_length=15,
        choices=(
            ('ADVERTISING', _('인원 모집 중')),
            ('ORDERED', _('주문 완료')),
            ('DELIVERING1', _('1차 배송 중')),
            ('DELIVERING2', _('2차 배송 중')),
            ('DELIVERED', _('배송 완료')),
            ('CANCELLED', _('취소됨')),
        ),
        default='ADVERTISING',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
