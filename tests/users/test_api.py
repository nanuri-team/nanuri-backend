import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserEndpoints:
    def test_list(self, user_client):
        users = UserFactory.create_batch(size=3)
        response = user_client.get(reverse("nanuri.users.api:list"))

        assert response.status_code == 200
        assert len(response.json()["results"]) == len(users) + 1

    def test_list_with_pagination(self, user_client):
        UserFactory.create_batch(size=100)
        response = user_client.get(
            reverse("nanuri.users.api:list"),
            data={"offset": "0", "limit": "20"},
        )

        assert response.status_code == 200
        assert len(response.json()["results"]) == 20

    def test_list_with_nickname(self, user_client):
        users = UserFactory.create_batch(size=3)
        user = users[0]
        response = user_client.get(
            reverse("nanuri.users.api:list"),
            data={"nickname": user.nickname},
        )

        assert response.status_code == 200
        count = response.json()["count"]
        results = response.json()["results"]
        assert count > 0
        assert len(results) > 0
        assert results[0]["nickname"] == user.nickname

    def test_create(self, user_client):
        user = UserFactory.build()
        response = user_client.post(
            reverse("nanuri.users.api:list"),
            data={
                "email": user.email,
                "password": user.password,
                "location": user.location.ewkt,
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == 201
        assert result["email"] == user.email
        assert "password" not in result
        assert result["location"] == user.location.ewkt

        created_user = get_user_model().objects.get(uuid=result["uuid"])
        assert check_password(user.password, created_user.password)

    def test_retrieve(self, user_client, user):
        response = user_client.get(
            reverse(
                "nanuri.users.api:detail",
                kwargs={"uuid": user.uuid},
            )
        )
        result = response.json()

        assert response.status_code == 200
        assert result["uuid"] == str(user.uuid)
        assert result["email"] == user.email
        assert result["location"] == user.location.ewkt

    def test_update(self, user_client, user):
        new_user = UserFactory.build()
        new_password = "password1234"
        fields = [
            "email",
            "nickname",
            "is_active",
            "is_admin",
            "address",
            "auth_provider",
            "location",
        ]
        data = {field: getattr(new_user, field) for field in fields}
        data["password"] = new_password
        data["location"] = data["location"].ewkt
        response = user_client.put(
            reverse("nanuri.users.api:detail", kwargs={"uuid": user.uuid}),
            data=data,
            format="json",
        )
        result = response.json()

        assert response.status_code == 200
        for field in fields:
            assert result[field] == getattr(new_user, field)

    @pytest.mark.parametrize(
        "field",
        [
            "email",
            "password",
            "nickname",
            "is_active",
            "is_admin",
            "address",
            "auth_provider",
            "location",
        ],
    )
    def test_partial_update(self, user_client, user, field):
        params = UserFactory.build()
        data = {field: getattr(params, field)}
        # location 필드는 location.ewkt 값이 할당되어야 함
        if field == "location":
            data[field] = data[field].ewkt
        if field == "password":
            data[field] = "1234"
        response = user_client.patch(
            reverse("nanuri.users.api:detail", kwargs={"uuid": user.uuid}),
            data=data,
            format="json",
        )
        result = response.json()
        if field == "password":
            updated_user = get_user_model().objects.get(uuid=result["uuid"])
            assert check_password("1234", updated_user.password)
        else:
            assert result[field] == getattr(params, field)

        assert response.status_code == 200

    def test_destroy(self, user_client, user):
        assert get_user_model().objects.filter(uuid=str(user.uuid)).count() == 1
        response = user_client.delete(
            reverse(
                "nanuri.users.api:detail",
                kwargs={"uuid": user.uuid},
            )
        )

        assert response.status_code == 204
        assert get_user_model().objects.filter(uuid=str(user.uuid)).count() == 0
