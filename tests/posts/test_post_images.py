import shutil

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestPostImageEndpoints:
    def test_upload_post_image(self, user_client, post):
        with open(str(settings.MEDIA_ROOT / "lena.tif"), "rb") as f:
            image_bytes = f.read()
        image_file = SimpleUploadedFile("test.tif", image_bytes, "image/tiff")
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

        shutil.rmtree(str(settings.MEDIA_ROOT / "posts"))
