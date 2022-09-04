import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
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
    image = Image.new("RGB", (100, 100), (0, 255, 0))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return SimpleUploadedFile("test.jpeg", buffer.getvalue(), "image/jpeg")


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
def subscription():
    return SubscriptionFactory.create()
