import pytest
from django.urls import reverse

from nanuri.notifications.models import Subscription

pytestmark = pytest.mark.django_db


class TestSubscriptionApi:
    base_url = "/api/v1"

    def test_create(self, user_client, device):
        response = user_client.post(
            reverse("nanuri.notifications.api:subscription-list"),
            data={
                "device": str(device.uuid),
                "topic": Subscription.Topic.TO_ALL,
                "group_code": None,
                "opt_in": True,
            },
            format="json",
        )
        assert response.status_code == 201

    def test_retrieve(self, user_client, subscription):
        response = user_client.get(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={"uuid": subscription.uuid},
            )
        )
        assert response.status_code == 200

    def test_delete(self, user_client, subscription):
        # FIXME: 실제 AWS 상에서도 구독이 취소(삭제)되었는지 테스트 필요...
        #  boto3로 로컬스택에 아무리 삭제 명령을 내려봐도 반응이 없는 버그가 있는듯
        assert Subscription.objects.filter(uuid=subscription.uuid).count() == 1
        response = user_client.delete(
            reverse(
                "nanuri.notifications.api:subscription-detail",
                kwargs={"uuid": subscription.uuid},
            )
        )
        assert response.status_code == 204
        assert Subscription.objects.filter(uuid=subscription.uuid).count() == 0
