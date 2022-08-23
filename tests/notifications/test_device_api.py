import pytest
from django.urls import reverse
from faker import Faker

from nanuri.aws.sns import sns
from nanuri.notifications.models import Device

from .factories import DeviceFactory, SubscriptionFactory

pytestmark = pytest.mark.django_db

fake = Faker()


class TestDeviceApi:
    base_url = "/api/v1"

    def test_create(self, user_client):
        device_token = fake.sha256()
        response = user_client.post(
            reverse("nanuri.notifications.api:device-list"),
            data={"device_token": device_token},
            format="json",
        )
        assert response.status_code == 201
        result = response.json()
        assert result["endpoint_arn"].startswith("arn:aws:sns")

    def test_retrieve(self, user_client, device):
        response = user_client.get(
            reverse(
                "nanuri.notifications.api:device-detail",
                kwargs={"uuid": device.uuid},
            ),
        )
        assert response.status_code == 200
        result = response.json()
        assert "user" in result
        assert result["device_token"] == device.device_token
        assert result["endpoint_arn"] == device.endpoint_arn

    def test_update(self, user_client, device):
        params = DeviceFactory.build()
        response = user_client.put(
            reverse(
                "nanuri.notifications.api:device-detail",
                kwargs={"uuid": device.uuid},
            ),
            data={"device_token": params.device_token},
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "field",
        [
            "device_token",
        ],
    )
    def test_partial_update(self, user_client, device, field):
        params = DeviceFactory.build()
        if field == "device_token":
            assert sns.get_endpoint_by_device_token(device.device_token) is not None
            assert sns.get_endpoint_by_device_token(params.device_token) is None
        response = user_client.patch(
            reverse(
                "nanuri.notifications.api:device-detail",
                kwargs={"uuid": device.uuid},
            ),
            data={field: getattr(params, field)},
        )
        assert response.status_code == 200
        if field == "device_token":
            assert sns.get_endpoint_by_device_token(device.device_token) is None
            assert sns.get_endpoint_by_device_token(params.device_token) is not None

    def test_delete(self, user_client, device):
        child_subscriptions = SubscriptionFactory.create_batch(size=3, device=device)
        assert len(device.subscription_set.all()) == 3

        assert sns.get_endpoint_by_device_token(device.device_token) is not None
        assert Device.objects.all().count() == 1

        response = user_client.delete(
            reverse(
                "nanuri.notifications.api:device-detail",
                kwargs={"uuid": device.uuid},
            )
        )
        assert response.status_code == 204

        assert Device.objects.all().count() == 0
        assert sns.get_endpoint_by_device_token(device.device_token) is None

        subscriptions = [x["SubscriptionArn"] for x in sns.list_subscriptions()]
        for child_subscription in child_subscriptions:
            assert child_subscription.subscription_arn not in subscriptions
