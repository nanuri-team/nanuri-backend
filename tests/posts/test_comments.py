import pytest
from django.urls import reverse

from nanuri.posts.models import Comment

from .factories import CommentFactory, PostFactory

pytestmark = pytest.mark.django_db


class TestCommentEndpoints:
    def test_list(self, user_client):
        post = PostFactory.create()
        comments = CommentFactory.create_batch(post=post, size=3)
        response = user_client.get(reverse("nanuri.posts.api:comment-list", kwargs={"uuid": post.uuid}))
        result = response.json()

        assert response.status_code == 200
        assert len(result["results"]) == len(comments)

    def test_create(self, user_client, user):
        post = PostFactory.create()
        comment = CommentFactory.build(post=post)
        response = user_client.post(
            reverse("nanuri.posts.api:comment-list", kwargs={"uuid": post.uuid}),
            data={
                "text": comment.text,
            },
            format="json",
        )
        result = response.json()

        assert response.status_code == 201

        created_comment = Comment.objects.get(uuid=result["uuid"])

        assert created_comment.post.uuid == post.uuid
        assert created_comment.text == comment.text
        assert created_comment.writer == user

    def test_retrieve(self, user_client, comment):
        response = user_client.get(
            reverse(
                "nanuri.posts.api:comment-detail",
                kwargs={"uuid": comment.post.uuid, "comment_uuid": comment.uuid},
            ),
        )
        assert response.status_code == 200

        result = response.json()
        assert result["uuid"] == str(comment.uuid)
        assert result["text"] == comment.text

    def test_update(self, user_client, comment):
        new_comment = CommentFactory.build()
        response = user_client.put(
            reverse(
                "nanuri.posts.api:comment-detail",
                kwargs={"uuid": comment.post.uuid, "comment_uuid": comment.uuid},
            ),
            data={"text": new_comment.text},
            format="json",
        )
        assert response.status_code == 200

        result = response.json()
        assert result["uuid"] == str(comment.uuid)
        assert result["text"] == new_comment.text

    def test_destroy(self, user_client, comment):
        assert Comment.objects.filter(uuid=str(comment.uuid)).count() == 1
        response = user_client.delete(
            reverse(
                "nanuri.posts.api:comment-detail",
                kwargs={"uuid": comment.post.uuid, "comment_uuid": comment.uuid},
            )
        )
        assert response.status_code == 204
        assert Comment.objects.filter(uuid=str(comment.uuid)).count() == 0
