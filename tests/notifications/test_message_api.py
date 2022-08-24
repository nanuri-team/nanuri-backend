import pytest
from django.urls import reverse
from faker import Faker

pytestmark = pytest.mark.django_db

fake = Faker()


class TestMessageApi:
    def test_publish_push_notification_message(self, user_client, post):
        response = user_client.post(
            reverse("nanuri.notifications.api:message-list"),
            data={
                "topic": "TO_CHAT_ROOM",
                "body": "Hello",
                "group_code": str(post.uuid),
            },
            format="json",
        )
        assert response.status_code == 204
