import shutil

import boto3
import pytest
from cryptography.hazmat.primitives.serialization.pkcs12 import load_pkcs12
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from OpenSSL.crypto import FILETYPE_PEM, dump_certificate, dump_privatekey, load_pkcs12
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
    endpoint_url=settings.AWS_ENDPOINT_URL,
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
    # for sub in sns.list_subscriptions()["Subscriptions"]:
    #     sub_arn = sub["SubscriptionArn"]
    #     sns.unsubscribe(SubscriptionArn=sub_arn)
    # for topic in sns.list_topics()["Topics"]:
    #     topic_arn = topic["TopicArn"]
    #     sns.delete_topic(TopicArn=topic_arn)
    for app in sns.list_platform_applications()["PlatformApplications"]:
        app_arn = app["PlatformApplicationArn"]
        # for endpoint in sns.list_endpoints_by_platform_application(
        #     PlatformApplicationArn=app_arn
        # )["Endpoints"]:
        #     endpoint_arn = endpoint["EndpointArn"]
        #     sns.delete_endpoint(EndpointArn=endpoint_arn)
        sns.delete_platform_application(PlatformApplicationArn=app_arn)


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
def p12():
    with open(str(settings.BASE_DIR / "certificate.p12"), "rb") as f:
        p12_bytes = f.read()
    return load_pkcs12(p12_bytes, b"")


@pytest.fixture
def p12_certificate(p12):
    return dump_certificate(FILETYPE_PEM, p12.get_certificate()).decode("utf-8")


@pytest.fixture
def p12_private_key(p12):
    return dump_privatekey(FILETYPE_PEM, p12.get_privatekey()).decode("utf-8")


@pytest.fixture
def sns_platform_application(p12_certificate, p12_private_key):
    return sns.create_platform_application(
        Name="TestApplication",
        Platform="APNS",
        Attributes={
            "PlatformCredential": p12_certificate,
            "PlatformPrincipal": p12_private_key,
        },
    )


@pytest.fixture
def device_token(sns_platform_application):
    return "b08f718bb925af6e3103d3c74a0275727e0112be1b70465dab1aed7c973ac308"


@pytest.fixture
def sns_platform_endpoint(sns_platform_application, device_token):
    return sns.create_platform_endpoint(
        PlatformApplicationArn=sns_platform_application["PlatformApplicationArn"],
        Token=device_token,
    )


@pytest.fixture
def device(device_token, sns_platform_endpoint):
    return DeviceFactory.create(
        device_token=device_token,
        endpoint_arn=sns_platform_endpoint["EndpointArn"],
    )


@pytest.fixture
def sns_topic():
    return sns.create_topic(Name="TestTopic")


@pytest.fixture
def sns_subscription(sns_topic, sns_platform_endpoint):
    return sns.subscribe(
        TopicArn=sns_topic["TopicArn"],
        Protocol="application",
        Endpoint=sns_platform_endpoint["EndpointArn"],
        ReturnSubscriptionArn=True,
    )


@pytest.fixture
def subscription(device, post, sns_subscription):
    return SubscriptionFactory.create(
        device=device,
        group_code=post.uuid,
        subscription_arn=sns_subscription["SubscriptionArn"],
    )
