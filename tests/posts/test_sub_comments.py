import pytest
from django.urls import reverse

from nanuri.posts.models import Comment, SubComment

from .factories import CommentFactory, SubCommentFactory

pytestmark = pytest.mark.django_db


class TestSubCommentEndpoints:
    def test_list(self, user_client, comment):
        sub_comments = SubCommentFactory.create_batch(comment=comment, size=3)
        response = user_client.get(reverse("nanuri.posts.api:sub-comment-list"))
        result = response.json()

        assert response.status_code == 200
        assert len(result["results"]) == len(sub_comments)

    def test_create(self, user_client, user):
        comment = CommentFactory.create()
        sub_comment = SubCommentFactory.build(comment=comment)
        response = user_client.post(
            reverse("nanuri.posts.api:sub-comment-list"),
            data={"comment": str(comment.uuid), "text": sub_comment.text},
            format="json",
        )
        result = response.json()

        assert response.status_code == 201

        created_sub_comment = SubComment.objects.get(uuid=result["uuid"])

        assert created_sub_comment.comment.uuid == comment.uuid
        assert created_sub_comment.text == sub_comment.text
        assert created_sub_comment.writer == user

    def test_retrieve(self, user_client, sub_comment):
        response = user_client.get(
            reverse(
                "nanuri.posts.api:sub-comment-detail",
                kwargs={"uuid": sub_comment.uuid},
            ),
        )
        assert response.status_code == 200

        result = response.json()
        assert result["uuid"] == str(sub_comment.uuid)
        assert result["text"] == sub_comment.text

    def test_update(self, user_client, sub_comment):
        new_comment = CommentFactory.create()
        new_sub_comment = SubCommentFactory.build()
        response = user_client.put(
            reverse(
                "nanuri.posts.api:sub-comment-detail",
                kwargs={"uuid": sub_comment.uuid},
            ),
            data={
                "comment": str(new_comment.uuid),
                "text": new_sub_comment.text,
            },
            format="json",
        )
        assert response.status_code == 200

        result = response.json()
        assert result["uuid"] == str(sub_comment.uuid)
        assert result["text"] == new_sub_comment.text

    def test_destroy(self, user_client, sub_comment):
        assert SubComment.objects.filter(uuid=str(sub_comment.uuid)).count() == 1
        response = user_client.delete(
            reverse(
                "nanuri.posts.api:sub-comment-detail",
                kwargs={"uuid": sub_comment.uuid},
            )
        )
        assert response.status_code == 204
        assert Comment.objects.filter(uuid=str(sub_comment.uuid)).count() == 0
