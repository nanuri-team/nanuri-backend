import boto3
from django.conf import settings
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from nanuri.posts.models import Post

from ..models import Device, Subscription
from .serializers import DeviceSerializer, SubscriptionSerializer

sns = boto3.client(
    "sns",
    endpoint_url=settings.AWS_ENDPOINT_URL,
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


@extend_schema_view(
    post=extend_schema(
        description="<h2>기기 정보를 등록합니다.</h2>",
        summary="Create a new device",
        tags=["Device"],
    ),
)
class DeviceCreateAPIView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        user = self.request.user
        device_token = self.request.data["device_token"]
        endpoint_arn = sns.create_platform_endpoint(
            PlatformApplicationArn=settings.AWS_SNS_PLATFORM_APPLICATION_ARN,
            Token=device_token,
        )["EndpointArn"]
        serializer.save(user=user, endpoint_arn=endpoint_arn)


@extend_schema_view(
    get=extend_schema(
        description="<h2>특정 기기 정보를 조회합니다.</h2>",
        summary="Get a device",
        tags=["Device"],
    ),
    put=extend_schema(
        description="<h2>특정 기기 정보를 수정합니다.</h2>",
        summary="Update a device",
        tags=["Device"],
    ),
    patch=extend_schema(
        description="<h2>특정 기기 정보를 부분 수정합니다.</h2>",
        summary="Patch a device",
        tags=["Device"],
    ),
    delete=extend_schema(
        description="<h2>특정 기기 정보를 삭제합니다.</h2>",
        summary="Delete a device",
        tags=["Device"],
    ),
)
class DeviceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
    lookup_field = "uuid"


@extend_schema_view(
    get=extend_schema(
        description="<h2>구독 목록을 조회합니다.</h2>",
        summary="Get list of subscriptions",
        tags=["Subscription"],
    ),
    post=extend_schema(
        description="<h2>구독을 생성합니다.</h2>",
        summary="Create a new subscription",
        tags=["Subscription"],
    ),
)
class SubscriptionListCreateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    lookup_url_kwarg = "device_uuid"

    def get_queryset(self):
        device_uuid = self.kwargs[self.lookup_url_kwarg]
        return Subscription.objects.filter(device__uuid=device_uuid)

    def perform_create(self, serializer):
        device_uuid = self.kwargs[self.lookup_url_kwarg]
        device = Device.objects.get(uuid=device_uuid)
        post_uuid = self.request.data["post"]
        post = Post.objects.get(uuid=post_uuid)
        topic = self.request.data["topic"]

        topic_arn = sns.create_topic(Name=f"{topic}-{post_uuid}")["TopicArn"]
        subscription_arn = sns.subscribe(
            TopicArn=topic_arn,
            Protocol="application",
            Endpoint=device.endpoint_arn,
        )["SubscriptionArn"]

        serializer.save(device=device, post=post, subscription_arn=subscription_arn)


@extend_schema_view(
    get=extend_schema(
        description="<h2>특정 구독을 조회합니다.</h2>",
        summary="Get a subscription",
        tags=["Subscription"],
    ),
    put=extend_schema(
        description="<h2>특정 구독을 수정합니다.</h2>",
        summary="Update a subscription",
        tags=["Subscription"],
    ),
    patch=extend_schema(
        description="<h2>특정 구독을 부분 수정합니다.</h2>",
        summary="Patch a subscription",
        tags=["Subscription"],
    ),
    delete=extend_schema(
        description="<h2>특정 구독을 삭제합니다.</h2>",
        summary="Delete a subscription",
        tags=["Subscription"],
    ),
)
class SubscriptionRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "device_uuid"

    def get_object(self):
        device_uuid = self.kwargs[self.lookup_url_kwarg]
        subscription_uuid = self.kwargs[self.lookup_field]
        return Subscription.objects.get(
            device__uuid=device_uuid,
            uuid=subscription_uuid,
        )
