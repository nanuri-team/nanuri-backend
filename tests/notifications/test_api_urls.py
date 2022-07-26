import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestNotificationApiUrls:
    base_url = "/api/v1"

    def test_device_list_url(self):
        url = reverse("nanuri.notifications.api:device-list")
        assert url == self.base_url + "/notifications/devices/"

    def test_device_detail_url(self, device):
        url = reverse(
            "nanuri.notifications.api:device-detail",
            kwargs={"uuid": device.uuid},
        )
        assert url == self.base_url + f"/notifications/devices/{device.uuid}/"

    def test_subscription_list_url(self, device):
        url = reverse(
            "nanuri.notifications.api:subscription-list",
            kwargs={"device_uuid": device.uuid},
        )
        assert (
            url
            == self.base_url + f"/notifications/devices/{device.uuid}/subscriptions/"
        )

    def test_subscription_detail_url(self, subscription):
        device = subscription.device
        url = reverse(
            "nanuri.notifications.api:subscription-detail",
            kwargs={"device_uuid": device.uuid, "uuid": subscription.uuid},
        )
        assert (
            url
            == self.base_url
            + f"/notifications/devices/{device.uuid}/subscriptions/{subscription.uuid}/"
        )
