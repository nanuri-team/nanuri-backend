from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    class Category(models.TextChoices):
        BATHROOM = "BATHROOM", _("욕실")
        FOOD = "FOOD", _("음식")
        KITCHEN = "KITCHEN", _("주방")
        HOUSEHOLD = "HOUSEHOLD", _("생활용품")
        STATIONERY = "STATIONERY", _("문구")
        ETC = "ETC", _("기타")

    class TradeType(models.TextChoices):
        DIRECT = "DIRECT", _("직거래")
        PARCEL = "PARCEL", _("택배 거래")

    class OrderStatus(models.TextChoices):
        WAITING = "WAITING", _("인원 모집 중")
        ORDERING = "ORDERING", _("주문 진행 중")
        ORDERED = "ORDERED", _("주문 완료")
        DELIVERING1 = "DELIVERING1", _("1차 배송 중")
        DELIVERING2 = "DELIVERING2", _("2차 배송 중")
        DELIVERED = "DELIVERED", _("배송 완료")
        CANCELLED = "CANCELLED", _("취소됨")

    def upload_to(self, filename):
        post_uuid = self.uuid
        ext = Path(filename).suffix
        return f"posts/{post_uuid}/{uuid4().hex[:8]}{ext}"

    uuid = models.UUIDField(
        verbose_name="uuid",
        unique=True,
        default=uuid4,
        editable=False,
    )
    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=255,
        choices=Category.choices,
        default=Category.ETC,
    )
    image = models.ImageField(
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
        choices=TradeType.choices,
        null=True,
        blank=True,
    )
    order_status = models.CharField(
        max_length=15,
        choices=OrderStatus.choices,
        default=OrderStatus.WAITING,
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveBigIntegerField(default=0)
    waited_from = models.DateField(null=True, blank=True, default=None)
    waited_until = models.DateField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # post.writer == 이 글의 작성자
    # user.posts.all() == 유저가 작성한 모든 글
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    # post.participants.all() == 이 글에 참여한 모든 유저
    # user.posts_participated.all() == 유저가 참여한 모든 글
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

    uuid = models.UUIDField(
        verbose_name="uuid",
        unique=True,
        default=uuid4,
        editable=False,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to=upload_to,
    )

    @property
    def image_url(self):
        return self.image.url


class Comment(models.Model):
    uuid = models.UUIDField(
        verbose_name="uuid",
        unique=True,
        default=uuid4,
        editable=False,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField()
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text[:10]}... by {self.writer}"


class SubComment(models.Model):
    uuid = models.UUIDField(
        verbose_name="uuid",
        unique=True,
        default=uuid4,
        editable=False,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="sub_comments",
    )
    text = models.TextField()
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text[:10]}... by {self.writer}"
