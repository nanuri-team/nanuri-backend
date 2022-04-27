import pytest
from django.urls import reverse

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

    def test_create(self, user_client):
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
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == 201
        assert result["title"] == post.title

        assert post.waited_from is not None
        assert post.waited_until is not None
        assert post.waited_from.strftime("%Y-%m-%d") == result["waited_from"]
        assert post.waited_from.strftime("%Y-%m-%d") == result["waited_until"]

    def test_retrieve(self, user_client, post):
        response = user_client.get(reverse("nanuri.posts.api:detail", kwargs={"uuid": post.uuid}))
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

    def test_destroy(self, user_client, post):
        assert Post.objects.filter(uuid=str(post.uuid)).count() == 1
        response = user_client.delete(reverse("nanuri.posts.api:detail", kwargs={"uuid": post.uuid}))

        assert response.status_code == 204
        assert Post.objects.filter(uuid=str(post.uuid)).count() == 0
