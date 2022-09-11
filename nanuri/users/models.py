import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class AuthProvider(models.TextChoices):
        APPLE = "APPLE", _("애플")
        KAKAO = "KAKAO", _("카카오")

    uuid = models.UUIDField(
        verbose_name="uuid",
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    address = models.CharField(max_length=255, null=True, blank=True, default=None)
    profile = models.ImageField(null=True, blank=True, default=None)
    auth_provider = models.CharField(
        max_length=15,
        choices=AuthProvider.choices,
        null=True,
        blank=True,
    )
    location = models.PointField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # user.favorite_posts.all() == 이 user가 즐겨찾기한 모든 글
    # post.favored_by.all() == 이 post를 좋아하는 모든 유저
    favorite_posts = models.ManyToManyField(
        "posts.Post",
        related_name="favored_by",
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
