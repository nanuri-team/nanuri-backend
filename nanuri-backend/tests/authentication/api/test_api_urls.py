import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestApiUrls:
    base_url = "/api"

    def test_user_list_url(self):
        url = reverse("nanuri.authentication:kakao-account-list")
        assert url == self.base_url + "/auth/kakao/accounts/"

    def test_token_url(self):
        url = reverse("nanuri.authentication:token_obtain_pair")
        assert url == self.base_url + "/auth/token/"

    def test_token_refresh_url(self):
        url = reverse("nanuri.authentication:token_refresh")
        assert url == self.base_url + "/auth/token/refresh/"

    def test_token_verify_url(self):
        url = reverse("nanuri.authentication:token_verify")
        assert url == self.base_url + "/auth/token/verify/"
