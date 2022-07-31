import pytest
from django.urls import reverse

from nanuri.notifications.models import Device

from .factories import DeviceFactory

pytestmark = pytest.mark.django_db


class TestDeviceApi:
    base_url = "/api/v1"

    def test_create(self, user_client, device_token):
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
        assert "device_token" in result
        assert "endpoint_arn" in result

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
        response = user_client.patch(
            reverse(
                "nanuri.notifications.api:device-detail",
                kwargs={"uuid": device.uuid},
            ),
            data={field: getattr(params, field)},
        )
        assert response.status_code == 200

    def test_delete(self, user_client, device):
        assert Device.objects.all().count() == 1
        response = user_client.delete(
            reverse(
                "nanuri.notifications.api:device-detail",
                kwargs={"uuid": device.uuid},
            )
        )
        assert response.status_code == 204
        assert Device.objects.all().count() == 0
