import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .posts.factories import PostFactory
from .users.factories import UserFactory


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
def token(user):
    return Token.objects.create(user=user)
