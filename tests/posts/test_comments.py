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
