import shutil

import boto3
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

sns = boto3.client(
    "sns",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


@pytest.fixture(autouse=True)
def run_around_tests():
    yield

    # 매 테스트 이후 생성된 미디어 파일 삭제
    post_media_dir = settings.MEDIA_ROOT / "posts"
    if post_media_dir.exists():
        shutil.rmtree(str(post_media_dir))

    # 매 테스트 이후 생성한 AWS SNS 주제, 구독 삭제
    for sub in sns.list_subscriptions()["Subscriptions"]:
        sub_arn = sub["SubscriptionArn"]
        sns.unsubscribe(SubscriptionArn=sub_arn)
    for topic in sns.list_topics()["Topics"]:
        topic_arn = topic["TopicArn"]
        sns.delete_topic(TopicArn=topic_arn)


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
    return DeviceFactory.create(
        device_token="b08f718bb925af6e3103d3c74a0275727e0112be1b70465dab1aed7c973ac308",
        endpoint_arn="arn:aws:sns:ap-northeast-2:833928806580:endpoint/APNS/TestApplication/91d08d28-8435-37bd-9819-cf9a3989b687",
    )


@pytest.fixture
def subscription(device, post):
    return SubscriptionFactory.create(device=device, post=post)
