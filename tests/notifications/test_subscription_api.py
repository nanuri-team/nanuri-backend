import pytest
from django.urls import reverse

from nanuri.notifications.models import Subscription

pytestmark = pytest.mark.django_db


class TestSubscriptionApi:
    base_url = "/api/v1"

    def test_create(self, user_client, device, post):
        response = user_client.post(
            reverse("nanuri.notifications.api:subscription-list"),
            data={
                "device": str(device.uuid),
                "post": str(post.uuid),
                "topic": Subscription.Topic.CHAT_MESSAGE_NOTIFICATIONS,
            },
            format="json",
        )
        assert response.status_code == 201

    def test_retrieve(self, user_client, subscription):
        response = user_client.get(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={"uuid": subscription.uuid},
            )
        )
        assert response.status_code == 200

    def test_delete(self, user_client, subscription):
        assert Subscription.objects.filter(uuid=subscription.uuid).count() == 1
        response = user_client.delete(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={"uuid": subscription.uuid},
            )
        )
        assert response.status_code == 204
        assert Subscription.objects.filter(uuid=subscription.uuid).count() == 0
