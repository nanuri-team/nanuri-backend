import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db


class TestAuthenticationEndpoints:
    kakao_id = 2164473263

    def test_save_user_and_get_token(self, user_client):
        response = user_client.post(
            reverse("nanuri.authentication:kakao-account-list"),
            data={"kakao_id": self.kakao_id},
            format="json",
        )
        assert response.status_code == 201

        result = response.json()
        assert result["type"] == "Token"
        assert "token" in result
        assert "uuid" in result

    def test_create_kakao_account_get_method_failed(self, user_client):
        response = user_client.get(reverse("nanuri.authentication:kakao-account-list"))
        assert response.status_code == 405

    def test_token_is_changed_every_creation_request(self, user_client):
        request_args = {
            "path": reverse("nanuri.authentication:kakao-account-list"),
            "data": {"kakao_id": self.kakao_id},
            "format": "json",
        }

        response = user_client.post(**request_args)
        assert response.status_code == 201
        token = response.json()["token"]
        assert Token.objects.filter(key=token).count() == 1

        response = user_client.post(**request_args)
        assert response.status_code == 201
        token2 = response.json()["token"]
        assert Token.objects.filter(key=token).count() == 0
        assert Token.objects.filter(key=token2).count() == 1

        assert token != token2
