import shutil

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .notifications.factories import DeviceFactory, SubscriptionFactory
from .posts.factories import (
    CommentFactory,
    PostFactory,
    PostImageFactory,
    SubCommentFactory,
)
from .users.factories import UserFactory


@pytest.fixture(autouse=True)
def run_around_tests():
    yield

    # 매 테스트 이후 생성된 미디어 파일 삭제
    post_media_dir = settings.MEDIA_ROOT / "posts"
    if post_media_dir.exists():
        shutil.rmtree(str(post_media_dir))


@pytest.fixture
def user():
    return UserFactory.create()


@pytest.fixture
def user_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def post():
    return PostFactory.create()


@pytest.fixture
def post_image(post):
    return PostImageFactory.create(post=post)


@pytest.fixture
def image_file():
    with open(str(settings.MEDIA_ROOT / "lena.tif"), "rb") as f:
        image_bytes = f.read()
    return SimpleUploadedFile("test.tif", image_bytes, "image/tiff")


@pytest.fixture
def token(user):
    return Token.objects.create(user=user)


@pytest.fixture
def comment(post):
    return CommentFactory.create(post=post)


@pytest.fixture
def sub_comment(comment):
    return SubCommentFactory.create(comment=comment)


@pytest.fixture
def device():
    return DeviceFactory.create()


@pytest.fixture
def subscription(device, post):
    return SubscriptionFactory.create(device=device, post=post)
