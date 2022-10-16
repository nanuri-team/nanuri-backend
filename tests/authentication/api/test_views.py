from unittest import mock

import pytest
from django.urls import reverse
from django.utils.timezone import now, timedelta
from faker import Faker
from freezegun import freeze_time
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.users.factories import UserFactory

pytestmark = pytest.mark.django_db

fake = Faker()


def mock_kakao_account_info(kakao_id):
    return {
        "kakao_account": {
            "is_email_valid": True,
            "is_email_verified": True,
            "email": "user@example.com",
        }
    }


@mock.patch(
    "nanuri.authentication.api.views.get_kakao_account_info",
    mock_kakao_account_info,
)
class TestAuthenticationEndpoints:
    kakao_id = fake.pyint(min_value=1_000_000_000, max_value=9_999_999_999)
    anonymous = APIClient()

    def test_save_user_and_get_token(self):
        response = self.anonymous.post(
            reverse("nanuri.authentication:kakao-account-list"),
            data={"kakao_id": self.kakao_id},
            format="json",
        )
        assert response.status_code == 201

        result = response.json()
        assert result["type"] == "Token"
        assert "token" in result
        assert "uuid" in result

    @pytest.mark.skip
    def test_save_user_and_get_jwt(self):
        response = self.anonymous.post(
            reverse("nanuri.authentication:kakao-account-list"),
            data={"kakao_id": self.kakao_id},
            format="json",
        )
        assert response.status_code == 201

        result = response.json()
        assert result["type"] == "Bearer"
        assert "access" in result
        assert "refresh" in result
        assert "uuid" in result

    def test_create_kakao_account_get_method_failed(self):
        response = self.anonymous.get(
            reverse("nanuri.authentication:kakao-account-list")
        )
        assert response.status_code == 405

    @pytest.mark.skip
    def test_token_is_changed_every_creation_request(self):
        request_args = {
            "path": reverse("nanuri.authentication:kakao-account-list"),
            "data": {"kakao_id": self.kakao_id},
            "format": "json",
        }

        response = self.anonymous.post(**request_args)
        assert response.status_code == 201
        token = response.json()["token"]
        assert Token.objects.filter(key=token).count() == 1

        response = self.anonymous.post(**request_args)
        assert response.status_code == 201
        token2 = response.json()["token"]
        assert Token.objects.filter(key=token).count() == 0
        assert Token.objects.filter(key=token2).count() == 1

        assert token != token2

    def test_jwt(self):
        # JWT 발급
        raw_password = fake.password()
        user = UserFactory.create(is_active=True, password=raw_password)
        response = self.anonymous.post(
            reverse("nanuri.authentication:token_obtain_pair"),
            data={"email": user.email, "password": raw_password},
            format="json",
        )
        assert response.status_code == 200
        response_data = response.json()
        assert "access" in response_data
        assert "refresh" in response_data

        access_token = response_data["access"]
        refresh_token = response_data["refresh"]

        # 액세스 토큰 유효성 검사
        response = self.anonymous.post(
            reverse("nanuri.authentication:token_verify"),
            data={"token": access_token},
            format="json",
        )
        assert response.status_code == 200
        assert response.json() == dict()

        # 액세스 토큰 만료
        after_access_token_expired = now() + timedelta(minutes=5)
        with freeze_time(after_access_token_expired):
            # 액세스 토큰 유효성 검사 실패 (만료됨)
            response = self.anonymous.post(
                reverse("nanuri.authentication:token_verify"),
                data={"token": access_token},
                format="json",
            )
            assert response.status_code == 401
            response_data = response.json()
            assert "code" in response_data
            assert "detail" in response_data

            # 리프레시 토큰으로 액세스 토큰 재발급
            response = self.anonymous.post(
                reverse("nanuri.authentication:token_refresh"),
                data={"refresh": refresh_token},
                format="json",
            )
            assert response.status_code == 200
            assert "access" in response.json()

        # 리프레시 토큰 만료
        after_refresh_token_expired = now() + timedelta(days=1)
        with freeze_time(after_refresh_token_expired):
            # 리프레시 토큰으로 액세스 토큰 재발급 시 실패
            response = self.anonymous.post(
                reverse("nanuri.authentication:token_refresh"),
                data={"refresh": refresh_token},
                format="json",
            )
            assert response.status_code == 401
