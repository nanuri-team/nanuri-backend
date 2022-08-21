import boto3
from django.conf import settings


class SimpleNotificationService:
    def __init__(self):
        self.client = boto3.client(
            "sns",
            endpoint_url=settings.AWS_ENDPOINT_URL,
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

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
            attributes["group_code"] = group_code
        return self.client.subscribe(
            TopicArn=topic_arn,
            Protocol="application",
            Endpoint=endpoint_arn,
            Attributes=attributes,
            ReturnSubscriptionArn=True,
        )

    def unsubscribe(self, subscription_arn):
        return self.client.unsubscribe(SubscriptionArn=subscription_arn)


sns = SimpleNotificationService()
