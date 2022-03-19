import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

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
    uuid = models.UUIDField(
        verbose_name='uuid',
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
    profile_url = models.URLField(null=True, blank=True)
    auth_provider = models.CharField(
        max_length=15,
        choices=(
            ('APPLE', _('애플')),
            ('KAKAO', _('카카오')),
        ),
        null=True,
        default=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
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
