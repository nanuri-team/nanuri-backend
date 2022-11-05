import pytest
from django.urls import reverse

from nanuri.aws.sns import sns
from nanuri.notifications.models import Device, Subscription

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

    @pytest.mark.parametrize("subscription_opt_in", [True, False])
    @pytest.mark.parametrize("device_opt_in", [True, False])
    def test_delete(self, user_client, device_opt_in, subscription_opt_in):
        # given: 1개의 기기과 3개의 구독을 생성함
        device = DeviceFactory.create(opt_in=device_opt_in)
        subscriptions = SubscriptionFactory.create_batch(
            size=3,
            device=device,
            opt_in=subscription_opt_in,
        )
        device_token = device.device_token
        subscription_arns = [s.subscription_arn for s in subscriptions]
        assert Device.objects.all().count() == 1
        assert Subscription.objects.filter(device=device).count() == 3

        # when: 기기를 삭제함
        response = user_client.delete(
            reverse(
                "nanuri.notifications.api:device-detail",
                kwargs={"uuid": device.uuid},
            )
        )
        assert response.status_code == 204

        # then: 기기, 구독 정보 모두 삭제되어야 함
        assert Device.objects.all().count() == 0
        assert Subscription.objects.filter(device=device).count() == 0

        assert sns.get_endpoint_by_device_token(device_token) is None
        all_subscriptions = [x["SubscriptionArn"] for x in sns.list_subscriptions()]
        for subscription_arn in subscription_arns:
            assert subscription_arn not in all_subscriptions
