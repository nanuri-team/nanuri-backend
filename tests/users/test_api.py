import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from .factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserEndpoints:
    def test_list(self, user_client):
        users = UserFactory.create_batch(size=3)
        response = user_client.get(reverse("nanuri.users.api:list"))

        assert response.status_code == 200
        assert len(response.json()["results"]) == len(users) + 1

    def test_create(self, user_client):
        user = UserFactory.build()
        response = user_client.post(
            reverse("nanuri.users.api:list"),
            data={
                "email": user.email,
                "password": user.password,
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == 201
        assert result["email"] == user.email

    def test_retrieve(self, user_client, user):
        response = user_client.get(reverse("nanuri.users.api:detail", kwargs={"uuid": user.uuid}))
        result = response.json()

        assert response.status_code == 200
        assert result["uuid"] == str(user.uuid)
        assert result["email"] == user.email

    def test_update(self, user_client, user):
        new_user = UserFactory.build()
        new_password = "password1234"
        fields = [
            "email",
            "nickname",
            "is_active",
            "is_admin",
            "latitude",
            "longitude",
            "address",
            "profile_url",
            "auth_provider",
        ]
        data = {field: getattr(new_user, field) for field in fields}
        data["password"] = new_password
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
            "nickname",
            "is_active",
            "is_admin",
            "latitude",
            "longitude",
            "address",
            "profile_url",
            "auth_provider",
        ],
    )
    def test_partial_update(self, user_client, user, field):
        params = UserFactory.build()
        response = user_client.patch(
            reverse("nanuri.users.api:detail", kwargs={"uuid": user.uuid}),
            data={field: getattr(params, field)},
            format="json",
        )
        result = response.json()

        assert response.status_code == 200
        assert result[field] == getattr(params, field)

    def test_destroy(self, user_client, user):
        assert get_user_model().objects.filter(uuid=str(user.uuid)).count() == 1
        response = user_client.delete(
            reverse("nanuri.users.api:detail", kwargs={"uuid": user.uuid})
        )

        assert response.status_code == 204
        assert get_user_model().objects.filter(uuid=str(user.uuid)).count() == 0
