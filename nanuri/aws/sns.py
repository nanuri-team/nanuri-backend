import boto3
from django.conf import settings

sns = boto3.client(
    "sns",
    endpoint_url=settings.AWS_ENDPOINT_URL,
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


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
