from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from ..models import User


def has_properties_all(user: dict) -> bool:
    return (
        "last_login" in user
        and "uuid" in user
        and "email" in user
        and "nickname" in user
        and "is_active" in user
        and "is_admin" in user
        and "latitude" in user
        and "longitude" in user
        and "profile_url" in user
        and "created_at" in user
        and "updated_at" in user
    )


class UserAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_client = APIClient()
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            nickname="Administrator",
            password="password1234",
        )
        admin_token = Token.objects.create(user=self.admin)
        self.admin_client.force_authenticate(user=self.admin, token=admin_token)

    def test_get_user_list(self):
        response = self.admin_client.get("/api/v1/users/")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue("count" in data)
        self.assertTrue("next" in data)
        self.assertTrue("previous" in data)
        self.assertTrue("results" in data)

        user = data["results"][0]
        self.assertTrue(has_properties_all(user))

        self.assertFalse("password" in user)

        response = APIClient().get("/api/v1/users/")
        self.assertEqual(response.status_code, 401)

    def test_create_user(self):
        response = self.admin_client.post(
            "/api/v1/users/",
            data={
                "email": "test1@example.com",
                "password": "password1234",
            },
        )
        self.assertEqual(response.status_code, 201)

        user = response.json()
        self.assertTrue(has_properties_all(user))

    def test_get_user(self):
        response = self.admin_client.get(f"/api/v1/users/{self.admin.uuid}/")
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertTrue(has_properties_all(user))

    def test_update_user(self):
        response = self.admin_client.put(
            f"/api/v1/users/{self.admin.uuid}/",
            data={
                "email": "user2@example.com",
                "password": "password1234",
            },
        )
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertTrue(has_properties_all(user))

        self.assertEqual(user["uuid"], str(self.admin.uuid))
        self.assertEqual(user["email"], "user2@example.com")

    def test_patch_user(self):
        response = self.admin_client.patch(
            f"/api/v1/users/{self.admin.uuid}/",
            data={
                "latitude": 123.456789,
                "longitude": 111.111111,
            },
        )
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user["latitude"], 123.456789)
        self.assertEqual(user["longitude"], 111.111111)

    def test_delete_user(self):
        response = self.admin_client.delete(f"/api/v1/users/{self.admin.uuid}/")
        self.assertEqual(response.status_code, 204)

        self.assertRaises(
            User.DoesNotExist,
            lambda: User.objects.get(uuid=self.admin.uuid),
        )
