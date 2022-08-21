import pytest
from django.urls import reverse

from nanuri.aws.sns import list_subscriptions
from nanuri.notifications.models import Subscription

pytestmark = pytest.mark.django_db


class TestSubscriptionApi:
    base_url = "/api/v1"

    def test_create(self, user_client, device):
        response = user_client.post(
            reverse("nanuri.notifications.api:subscription-list"),
            data={
                "device": str(device.uuid),
                "topic": Subscription.Topic.TO_ALL,
                "group_code": None,
                "opt_in": True,
            },
            format="json",
        )
        assert response.status_code == 201
        result = response.json()
        assert result["subscription_arn"] in [
            x["SubscriptionArn"] for x in list_subscriptions()
        ]

    def test_retrieve(self, user_client, subscription):
        response = user_client.get(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={"uuid": subscription.uuid},
            )
        )
        assert response.status_code == 200

    def test_delete(self, user_client, subscription):
        assert subscription.subscription_arn in [
            x["SubscriptionArn"] for x in list_subscriptions()
        ]
        assert Subscription.objects.filter(uuid=subscription.uuid).count() == 1
        response = user_client.delete(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={"uuid": subscription.uuid},
            )
        )
        assert response.status_code == 204
        assert Subscription.objects.filter(uuid=subscription.uuid).count() == 0
        assert subscription.subscription_arn not in [
            x["SubscriptionArn"] for x in list_subscriptions()
        ]
