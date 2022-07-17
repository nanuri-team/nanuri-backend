import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestPostImageEndpoints:
    def test_upload_post_image(self, user_client, post, image_file):
        response = user_client.post(
            reverse("nanuri.posts.api:image-list", kwargs={"uuid": post.uuid}),
            data={"image": image_file},
        )
        assert response.status_code == 201

        result = response.json()
        image_uuid = result["uuid"]
        response = user_client.get(
            reverse(
                "nanuri.posts.api:image-detail",
                kwargs={
                    "uuid": post.uuid,
                    "image_uuid": image_uuid,
                },
            )
        )
        assert response.status_code == 200
