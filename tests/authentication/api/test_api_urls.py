import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestApiUrls:
    base_url = "/api"

    def test_user_list_url(self):
        url = reverse("nanuri.authentication:kakao-account-list")
        assert url == self.base_url + "/auth/kakao/accounts/"
