from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    def upload_to(self, filename):
        post_uuid = self.uuid
        ext = Path(filename).suffix
        return f"posts/{post_uuid}/{uuid4().hex[:8]}{ext}"

    uuid = models.UUIDField(
        verbose_name='uuid',
        unique=True,
        default=uuid4,
        editable=False,
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(
        unique=True,
        null=True,
        blank=True,
        default=None,
        upload_to=upload_to,
    )
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
    order_status = models.CharField(
        max_length=15,
        choices=(
            ('ADVERTISING', _('인원 모집 중')),
            ('ORDERING', _('주문 진행 중')),
            ('ORDERED', _('주문 완료')),
            ('DELIVERING1', _('1차 배송 중')),
            ('DELIVERING2', _('2차 배송 중')),
            ('DELIVERED', _('배송 완료')),
            ('CANCELLED', _('취소됨')),
        ),
        default='ADVERTISING',
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # post.writer == 이 글의 작성자
    # user.posts.all() == 이 유저가 작성한 모든 글
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    category = models.OneToOneField(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    # post.participants.all() == 이 글에 참여한 모든 유저
    # user.posts_participated.all() == 이 유저가 참여한 모든 글
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="posts_participated",
        blank=True,
    )

    def __str__(self):
        return self.title


class PostImage(models.Model):
    def upload_to(self, filename):
        post_uuid = self.post.uuid
        ext = Path(filename).suffix
        return f"posts/{post_uuid}/{uuid4().hex[:8]}{ext}"

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        unique=True,
        null=True,
        blank=True,
        default=None,
        upload_to=upload_to,
    )
