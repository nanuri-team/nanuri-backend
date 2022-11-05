import pytest
from django.urls import reverse

from nanuri.aws.sns import sns
from nanuri.notifications.models import Subscription

from .factories import DeviceFactory, SubscriptionFactory

pytestmark = pytest.mark.django_db


class TestSubscriptionApi:
    @pytest.mark.parametrize("subscription_opt_in", [True, False])
    @pytest.mark.parametrize("device_opt_in", [True, False])
    def test_create(self, user_client, device_opt_in, subscription_opt_in):
        # given: 1개의 기기를 준비함
        device = DeviceFactory.create(opt_in=device_opt_in)

        # when: 구독을 생성함
        response = user_client.post(
            reverse("nanuri.notifications.api:subscription-list"),
            data={
                "device": str(device.uuid),
                "topic": Subscription.Topic.TO_ALL,
                "group_code": None,
                "opt_in": subscription_opt_in,
            },
            format="json",
        )

        # then
        assert response.status_code == 201

        # `opt_in` 에 따라서 Subscription ARN 도 생성되어야 함
        result = response.json()
        if device_opt_in and subscription_opt_in:
            assert result["subscription_arn"].startswith("arn:aws:sns:")
            subscriptions = [x["SubscriptionArn"] for x in sns.list_subscriptions()]
            assert result["subscription_arn"] in subscriptions
        else:
            assert result["subscription_arn"] is None

    def test_retrieve(self, user_client, subscription):
        response = user_client.get(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={"uuid": subscription.uuid},
            )
        )
        assert response.status_code == 200

    def test_update(self, user_client, subscription, device):
        params = SubscriptionFactory.build()
        response = user_client.put(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={"uuid": subscription.uuid},
            ),
            data={
                "device": device.uuid,
                "topic": params.topic,
                "group_code": params.group_code,
            },
        )
        assert response.status_code == 200

        updated_subscription = Subscription.objects.get(uuid=subscription.uuid)
        assert updated_subscription.device.uuid == device.uuid
        assert updated_subscription.topic == params.topic
        assert updated_subscription.group_code == params.group_code

        subscriptions = [x["SubscriptionArn"] for x in sns.list_subscriptions()]
        if updated_subscription.opt_in:
            assert updated_subscription.subscription_arn in subscriptions
        assert subscription.subscription_arn not in subscriptions

    def test_delete(self, user_client, subscription):
        assert Subscription.objects.filter(uuid=subscription.uuid).count() == 1
        previous_subscription_arn = subscription.subscription_arn

        response = user_client.delete(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={"uuid": subscription.uuid},
            )
        )
        assert response.status_code == 204
        assert Subscription.objects.filter(uuid=subscription.uuid).count() == 0
        subscriptions = [x["SubscriptionArn"] for x in sns.list_subscriptions()]
        assert previous_subscription_arn not in subscriptions

    def test_opt_in_off(self, user_client):
        # given: 구독을 생성함
        subscription = SubscriptionFactory.create(opt_in=True)
        all_subscriptions = [x["SubscriptionArn"] for x in sns.list_subscriptions()]
        assert subscription.subscription_arn in all_subscriptions

        # when: `opt_in` 을 끔
        response = user_client.patch(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={"uuid": subscription.uuid},
            ),
            data={"opt_in": False},
            format="json",
        )

        # then
        assert response.status_code == 200

        all_subscriptions = [x["SubscriptionArn"] for x in sns.list_subscriptions()]
        assert subscription.subscription_arn not in all_subscriptions
