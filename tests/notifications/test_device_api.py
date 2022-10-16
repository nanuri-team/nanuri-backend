import pytest
from django.urls import reverse

from nanuri.aws.sns import sns
from nanuri.notifications.models import Device

from .factories import DeviceFactory, SubscriptionFactory

pytestmark = pytest.mark.django_db


class TestDeviceApi:
    @pytest.mark.parametrize("opt_in", [True, False])
    def test_create(self, user_client, opt_in):
        params = DeviceFactory.build(opt_in=opt_in)
        response = user_client.post(
            reverse("nanuri.notifications.api:device-list"),
            data={
                "device_token": params.device_token,
                "opt_in": params.opt_in,
            },
            format="json",
        )
        assert response.status_code == 201
        result = response.json()
        if params.opt_in:
            assert result["endpoint_arn"].startswith("arn:aws:sns")
        else:
            assert result["endpoint_arn"] is None

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

    @pytest.mark.parametrize("opt_in", [True, False])
    def test_update(self, user_client, device, opt_in):
        params = DeviceFactory.build(opt_in=opt_in)
        response = user_client.put(
            reverse(
                "nanuri.notifications.api:device-detail",
                kwargs={"uuid": device.uuid},
            ),
            data={
                "device_token": params.device_token,
                "opt_in": params.opt_in,
            },
            format="json",
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["device_token"] == params.device_token
        assert response_data["opt_in"] is params.opt_in

        endpoint = sns.get_endpoint_by_device_token(params.device_token)
        if params.opt_in:
            assert endpoint is not None
        else:
            assert endpoint is None

    @pytest.mark.parametrize("opt_in", [True, False])
    @pytest.mark.parametrize("field", ["device_token", "opt_in"])
    def test_partial_update(self, user_client, device, field, opt_in):
        params = DeviceFactory.build(opt_in=opt_in)

        response = user_client.patch(
            reverse(
                "nanuri.notifications.api:device-detail",
                kwargs={"uuid": device.uuid},
            ),
            data={field: getattr(params, field)},
            format="json",
        )

        assert response.status_code == 200
        response_data = response.json()

        updated_device = Device.objects.get(uuid=device.uuid)

        assert (
            response_data[field]
            == getattr(params, field)
            == getattr(updated_device, field)
        )

        endpoint = sns.get_endpoint_by_device_token(updated_device.device_token)
        if updated_device.opt_in:
            assert endpoint is not None
        else:
            assert endpoint is None

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
