import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import connection
from django.urls import reverse
from rest_framework.test import APIClient

from nanuri.posts.models import Post

from .factories import PostFactory

pytestmark = pytest.mark.django_db


class TestPostEndpoints:
    def test_list(self, user_client):
        posts = PostFactory.create_batch(size=3)
        response = user_client.get(reverse("nanuri.posts.api:list"))
        result = response.json()

        assert response.status_code == 200
        assert len(result["results"]) == len(posts)

    def test_list_with_pagination(self, user_client):
        PostFactory.create_batch(size=21)
        response = user_client.get(
            reverse("nanuri.posts.api:list"),
            data={"offset": "0", "limit": "20"},
        )
        result = response.json()

        assert response.status_code == 200
        assert len(result["results"]) == 20

    # FIXME: Raw SQL 쿼리 날리지 말고 함수로 거리 계산하도록 수정하기
    #  django.contrib.gis.geos.Point 클래스에서 제공하는 distance 메서드는 2d 거리를 계산해서 정확하지 않음
    @pytest.mark.skipif(
        condition=settings.DATABASES["default"]["ENGINE"]
        != "django.contrib.gis.db.backends.postgis",
        reason="PostGIS 데이터베이스를 사용하지 않습니다",
    )
    def test_list_nearby_posts_only(self, user):
        user_client = APIClient()
        user_client.force_authenticate(user=user)
        PostFactory.create_batch(size=100)
        max_distance_in_meter = 5000 * 1000  # (= 5,000 km)

        response = user_client.get(
            reverse("nanuri.posts.api:list"),
            data={
                "distance": max_distance_in_meter,
            },
        )

        assert response.status_code == 200
        with connection.cursor() as cursor:
            for result in response.json()["results"]:
                writer = get_user_model().objects.get(email=result["writer"]["email"])
                sql = (
                    "SELECT ST_DistanceSphere("
                    "'SRID=4326;POINT (%s %s)'::geometry, "
                    "'SRID=4326;POINT (%s %s)'::geometry)"
                )
                cursor.execute(
                    sql,
                    [
                        user.location.x,
                        user.location.y,
                        writer.location.x,
                        writer.location.y,
                    ],
                )
                row = cursor.fetchone()
                assert row is not None
                distance = row[0]
                assert distance < max_distance_in_meter

    def test_list_by_category(self, user_client):
        for category in Post.Category.values:
            PostFactory.create_batch(size=2, category=category)

        response = user_client.get(
            reverse("nanuri.posts.api:list"),
            {"category": Post.Category.FOOD.name},
        )

        results = response.json()["results"]
        assert len(results) == 2

    def test_create(self, user_client, image_file):
        post = PostFactory.build()
        num_post_images = 3
        response = user_client.post(
            reverse("nanuri.posts.api:list"),
            data={
                "title": post.title,
                "unit_price": post.unit_price,
                "quantity": post.quantity,
                "description": post.description,
                "min_participants": post.min_participants,
                "max_participants": post.max_participants,
                # "num_participants": post.num_participants,
                "product_url": post.product_url,
                "trade_type": post.trade_type,
                "order_status": post.order_status,
                "is_published": post.is_published,
                # "published_at": post.published_at,
                # "view_count": post.view_count,
                "waited_from": post.waited_from,
                "waited_until": post.waited_until,
                "image": image_file,
                "images": [image_file for _ in range(num_post_images)],
            },
            format="multipart",
        )

        assert response.status_code == 201
        result = response.json()

        assert result["title"] == post.title
        assert len(result["images"]) == num_post_images

        created_post = Post.objects.get(uuid=result["uuid"])

        assert created_post.waited_from is not None
        assert created_post.waited_until is not None
        assert created_post.waited_from.strftime("%Y-%m-%d") == result["waited_from"]
        assert created_post.waited_until.strftime("%Y-%m-%d") == result["waited_until"]
        assert created_post.writer in created_post.participants.all()
        assert len(created_post.images.all()) == num_post_images

    def test_create_without_attached_images(self, user_client, image_file):
        post = PostFactory.build()
        response = user_client.post(
            reverse("nanuri.posts.api:list"),
            data={
                "title": post.title,
                "unit_price": post.unit_price,
                "quantity": post.quantity,
                "description": post.description,
                "min_participants": post.min_participants,
                "max_participants": post.max_participants,
                # "num_participants": post.num_participants,
                "product_url": post.product_url,
                "trade_type": post.trade_type,
                "order_status": post.order_status,
                "is_published": post.is_published,
                # "published_at": post.published_at,
                # "view_count": post.view_count,
                "waited_from": post.waited_from,
                "waited_until": post.waited_until,
                "image": image_file,
            },
            format="multipart",
        )
        assert response.status_code == 201

    def test_retrieve(self, user_client, post):
        response = user_client.get(
            reverse(
                "nanuri.posts.api:detail",
                kwargs={"uuid": post.uuid},
            )
        )
        result = response.json()

        assert response.status_code == 200
        assert result["uuid"] == str(post.uuid)
        assert result["title"] == post.title

    def test_update(self, user_client, post):
        new_post = PostFactory.build()
        fields = [
            "title",
            "unit_price",
            "quantity",
            "description",
            "min_participants",
            "max_participants",
            "product_url",
            "trade_type",
            "order_status",
            "is_published",
        ]
        response = user_client.put(
            reverse("nanuri.posts.api:detail", kwargs={"uuid": post.uuid}),
            data={field: getattr(new_post, field) for field in fields},
            format="json",
        )
        result = response.json()

        assert response.status_code == 200
        for field in fields:
            assert result[field] == getattr(new_post, field)

    @pytest.mark.parametrize(
        "field",
        [
            "title",
            "unit_price",
            "quantity",
            "description",
            "min_participants",
            "max_participants",
            "product_url",
            "trade_type",
            "order_status",
            "is_published",
        ],
    )
    def test_partial_update(self, user_client, post, field):
        params = PostFactory.build()
        response = user_client.patch(
            reverse("nanuri.posts.api:detail", kwargs={"uuid": post.uuid}),
            data={field: getattr(params, field)},
            format="json",
        )
        result = response.json()

        assert response.status_code == 200
        assert result[field] == getattr(params, field)

    def test_update_post_images(self, user_client, post, image_file):
        num_post_images = 2
        for _ in range(2):
            response = user_client.patch(
                reverse("nanuri.posts.api:detail", kwargs={"uuid": post.uuid}),
                data={"images": [image_file for _ in range(num_post_images)]},
                format="multipart",
            )
            assert response.status_code == 200
            result = response.json()

            assert len(result["images"]) == num_post_images

    def test_destroy(self, user_client, post):
        assert Post.objects.filter(uuid=str(post.uuid)).count() == 1
        response = user_client.delete(
            reverse(
                "nanuri.posts.api:detail",
                kwargs={"uuid": post.uuid},
            )
        )

        assert response.status_code == 204
        assert Post.objects.filter(uuid=str(post.uuid)).count() == 0
