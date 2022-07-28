import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestApiUrls:
    base_url = "/api/v1"

    def test_post_list_url(self):
        url = reverse("nanuri.posts.api:list")
        assert url == self.base_url + "/posts/"

    def test_post_detail_url(self, post):
        url = reverse("nanuri.posts.api:detail", kwargs={"uuid": post.uuid})
        assert url == self.base_url + f"/posts/{post.uuid}/"

    def test_comment_list_urls(self, post):
        url = reverse("nanuri.posts.api:comment-list")
        assert url == self.base_url + f"/posts/comments/"

    def test_comment_detail_urls(self, comment):
        url = reverse(
            "nanuri.posts.api:comment-detail",
            kwargs={"uuid": comment.uuid},
        )
        assert url == self.base_url + f"/posts/comments/{comment.uuid}/"

    def test_sub_comment_list_urls(self, comment):
        url = reverse("nanuri.posts.api:sub-comment-list")
        assert url == self.base_url + f"/posts/sub-comments/"

    def test_sub_comment_detail_urls(self, sub_comment):
        url = reverse(
            "nanuri.posts.api:sub-comment-detail",
            kwargs={"uuid": sub_comment.uuid},
        )
        assert url == self.base_url + f"/posts/sub-comments/{sub_comment.uuid}/"
