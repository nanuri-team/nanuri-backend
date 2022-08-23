import json
import os

import boto3
from django.conf import settings
from OpenSSL.crypto import FILETYPE_PEM, dump_certificate, dump_privatekey, load_pkcs12


class SimpleNotificationService:
    def __init__(self):
        self.client = boto3.client(
            "sns",
            endpoint_url=settings.AWS_ENDPOINT_URL,
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def create_platform_application(self, cert_path, name):
        if not os.path.exists(cert_path):
            return None
        with open(cert_path, "rb") as f:
            p12_bytes = f.read()
        p12 = load_pkcs12(p12_bytes)
        cert = dump_certificate(FILETYPE_PEM, p12.get_certificate()).decode("utf-8")
        key = dump_privatekey(FILETYPE_PEM, p12.get_privatekey()).decode("utf-8")
        platform_application = self.client.create_platform_application(
            Name=name,
            Platform="APNS",
            Attributes={
                "PlatformPrincipal": cert,
                "PlatformCredential": key,
            },
        )
        return platform_application["PlatformApplicationArn"]

    def create_platform_endpoint(self, device_token):
        if os.environ["DJANGO_SETTINGS_MODULE"] != "config.settings.prod":
            cert_path = settings.BASE_DIR / "certificate.p12"
            platform_application_arn = self.create_platform_application(
                cert_path, "TestApplication"
            )
            if platform_application_arn:
                settings.AWS_SNS_PLATFORM_APPLICATION_ARN = platform_application_arn

        platform_endpoint = self.client.create_platform_endpoint(
            PlatformApplicationArn=settings.AWS_SNS_PLATFORM_APPLICATION_ARN,
            Token=device_token,
        )
        return platform_endpoint["EndpointArn"]

    def get_or_create_platform_endpoint(self, device_token):
        endpoint = self.get_endpoint_by_device_token(device_token)
        endpoint_arn = (
            self.create_platform_endpoint(device_token)
            if endpoint is None
            else endpoint["EndpointArn"]
        )
        return endpoint_arn

    def list_endpoints(self):
        params = {}
        endpoints = []
        while True:
            response = self.client.list_endpoints_by_platform_application(
                PlatformApplicationArn=settings.AWS_SNS_PLATFORM_APPLICATION_ARN,
                **params,
            )
            items = response.get("Endpoints", [])
            endpoints.extend(items)
            if next_token := response.get("NextToken", None):
                params["NextToken"] = next_token
                continue
            break
        return endpoints

    def get_endpoint_by_device_token(self, device_token):
        endpoints = self.list_endpoints()
        for endpoint in endpoints:
            if endpoint["Attributes"]["Token"] == device_token:
                return endpoint
        return None

    def delete_endpoint(self, endpoint_arn):
        self.client.delete_endpoint(EndpointArn=endpoint_arn)

    def delete_endpoint_by_device_token(self, device_token):
        endpoint = self.get_endpoint_by_device_token(device_token)
        if endpoint is not None:
            self.delete_endpoint(endpoint["EndpointArn"])

    def create_topic(self, name):
        return self.client.create_topic(Name=name)

    def list_subscriptions(self):
        subscriptions = []
        params = {}
        while True:
            response = self.client.list_subscriptions(**params)
            subscriptions.extend(response.get("Subscriptions", []))
            if "NextToken" not in response:
                break
            params = {"NextToken": response["NextToken"]}
        return subscriptions

    def subscribe(self, topic, endpoint_arn, group_code):
        topic_arn = self.create_topic(topic)["TopicArn"]
        attributes = {}
        if group_code is not None:
            attributes["FilterPolicy"] = json.dumps({"group_code": group_code})
        subscription = self.client.subscribe(
            TopicArn=topic_arn,
            Protocol="application",
            Endpoint=endpoint_arn,
            Attributes=attributes,
            ReturnSubscriptionArn=True,
        )
        return subscription["SubscriptionArn"]

    def unsubscribe(self, subscription_arn):
        return self.client.unsubscribe(SubscriptionArn=subscription_arn)


sns = SimpleNotificationService()
