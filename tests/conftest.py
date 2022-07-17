import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .posts.factories import CommentFactory, PostFactory, PostImageFactory, SubCommentFactory
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
def post_image(post):
    return PostImageFactory.create(post=post)


@pytest.fixture
def token(user):
    return Token.objects.create(user=user)


@pytest.fixture
def comment(post):
    return CommentFactory(post=post)


@pytest.fixture
def sub_comment(comment):
    return SubCommentFactory(comment=comment)
