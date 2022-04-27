import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestUserEndpoints:
    def test_save_user_and_get_token(self, user_client):
        response = user_client.post(
            reverse("nanuri.authentication:kakao-account-list"),
            data={"kakao_id": 2164473263},
            format="json",
        )
        assert response.status_code == 201
        assert "token" in response.json()

    def test_create_kakao_account_get_method_failed(self, user_client):
        response = user_client.get(reverse("nanuri.authentication:kakao-account-list"))
        assert response.status_code == 405
