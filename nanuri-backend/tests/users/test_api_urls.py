import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestApiUrls:
    base_url = "/api/v1"

    def test_user_list_url(self):
        url = reverse("nanuri.users.api:list")
        assert url == self.base_url + "/users/"

    def test_user_detail_url(self, user):
        url = reverse("nanuri.users.api:detail", kwargs={"uuid": user.uuid})
        assert url == self.base_url + f"/users/{user.uuid}/"
