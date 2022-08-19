import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from OpenSSL.crypto import FILETYPE_PEM, dump_certificate, dump_privatekey, load_pkcs12

from nanuri.aws.s3 import s3

logger = logging.getLogger()

sns = boto3.client(
    "sns",
    endpoint_url=settings.AWS_ENDPOINT_URL,
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def create_platform_application():
    cert_path = "/tmp/certificate.p12"
    with open(cert_path, "wb") as f:
        s3.download_fileobj(
            settings.AWS_S3_CERTIFICATE_BUCKET_NAME,
            settings.AWS_S3_CERTIFICATE_KEY,
            f,
        )
    with open(cert_path, "rb") as f:
        p12_bytes = f.read()
    p12 = load_pkcs12(p12_bytes, b"")
    p12_certificate = dump_certificate(FILETYPE_PEM, p12.get_certificate()).decode(
        "utf-8"
    )
    p12_private_key = dump_privatekey(FILETYPE_PEM, p12.get_privatekey()).decode(
        "utf-8"
    )
    platform_application_arn = sns.create_platform_application(
        Name="TestApplication",
        Platform="APNS",
        Attributes={
            "PlatformCredential": p12_certificate,
            "PlatformPrincipal": p12_private_key,
        },
    )["PlatformApplicationArn"]
    settings.AWS_SNS_PLATFORM_APPLICATION_ARN = platform_application_arn
    return platform_application_arn


def create_platform_endpoint(device_token):
    """성공적으로 생성한 경우에만 arn 반환, 그 외는 null 반환"""
    try:
        response = sns.create_platform_endpoint(
            PlatformApplicationArn=settings.AWS_SNS_PLATFORM_APPLICATION_ARN,
            Token=device_token,
        )
        return response.get("EndpointArn", None)
    except ClientError as e:
        logger.error(e, exc_info=True)
    return None


def list_platform_endpoints(arn_only=False):
    endpoints = []
    params = {}
    while True:
        response = sns.list_endpoints_by_platform_application(
            PlatformApplicationArn=settings.AWS_SNS_PLATFORM_APPLICATION_ARN,
            **params,
        )
        endpoints.extend(response.get("Endpoints", []))
        if "NextToken" not in response:
            break
        params = {"NextToken": response["NextToken"]}
    if arn_only:
        return [x["EndpointArn"] for x in endpoints]
    return endpoints


def list_subscriptions(arn_only=False):
    subscriptions = []
    params = {}
    while True:
        response = sns.list_subscriptions(**params)
        subscriptions.extend(response.get("Subscriptions", []))
        if "NextToken" not in response:
            break
        params = {"NextToken": response["NextToken"]}
    if arn_only:
        return [x["SubscriptionArn"] for x in subscriptions]
    return subscriptions


def unsubscribe(subscription_arn):
    return sns.unsubscribe(SubscriptionArn=subscription_arn)


create_platform_application()
