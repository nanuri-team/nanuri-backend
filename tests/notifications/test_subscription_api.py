import pytest
from django.urls import reverse

from nanuri.notifications.models import Subscription

from ..posts.factories import PostFactory
from .factories import SubscriptionFactory

pytestmark = pytest.mark.django_db


class TestSubscriptionApi:
    base_url = "/api/v1"

    def test_create(self, user_client, device, post):
        response = user_client.post(
            reverse(
                "nanuri.notifications.api:subscription-list",
                kwargs={"device_uuid": device.uuid},
            ),
            data={"post": str(post.uuid)},
            format="json",
        )
        assert response.status_code == 201

    def test_retrieve(self, user_client, subscription):
        response = user_client.get(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={
                    "uuid": subscription.uuid,
                    "device_uuid": subscription.device.uuid,
                },
            )
        )
        assert response.status_code == 200

    def test_update(self, user_client, subscription):
        new_post = PostFactory.create()
        params = SubscriptionFactory.build()
        response = user_client.put(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={
                    "uuid": subscription.uuid,
                    "device_uuid": subscription.device.uuid,
                },
            ),
            data={
                "post": str(new_post.uuid),
                "receive_chat_messages": params.receive_chat_messages,
                "receive_comments": params.receive_comments,
            },
        )
        assert response.status_code == 200

        result = response.json()
        assert result["post"] == str(new_post.uuid)
        assert result["receive_chat_messages"] == params.receive_chat_messages
        assert result["receive_comments"] == params.receive_comments

    @pytest.mark.parametrize(
        "field",
        [
            "receive_chat_messages",
            "receive_comments",
        ],
    )
    def test_partial_update(self, user_client, subscription, post, field):
        params = SubscriptionFactory.build()
        response = user_client.patch(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={
                    "uuid": subscription.uuid,
                    "device_uuid": subscription.device.uuid,
                },
            ),
            data={field: getattr(params, field)},
        )
        assert response.status_code == 200

    def test_update_post_only(self, user_client, subscription):
        new_post = PostFactory.create()
        response = user_client.patch(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={
                    "uuid": subscription.uuid,
                    "device_uuid": subscription.device.uuid,
                },
            ),
            data={"post": str(new_post.uuid)},
        )
        assert response.status_code == 200

    def test_delete(self, user_client, subscription):
        assert Subscription.objects.filter(uuid=subscription.uuid).count() == 1
        response = user_client.delete(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={
                    "uuid": subscription.uuid,
                    "device_uuid": subscription.device.uuid,
                },
            )
        )
        assert response.status_code == 204
        assert Subscription.objects.filter(uuid=subscription.uuid).count() == 0
