from django.conf import settings
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from nanuri.aws.sns import client as sns_client

from ..models import Device, Subscription
from .serializers import DeviceSerializer, SubscriptionSerializer


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
        endpoint_arn = sns_client.create_platform_endpoint(
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
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return Device.objects.get(uuid=uuid)


@extend_schema_view(
    get=extend_schema(
        description="<h2>구독 목록을 조회합니다.</h2>",
        summary="Get list of subscriptions",
        tags=["Subscription"],
        parameters=[
            OpenApiParameter(
                name="device",
                location=OpenApiParameter.QUERY,
                description="Device UUID",
                required=False,
                type=str,
            )
        ],
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
    pagination_class = LimitOffsetPagination
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        queryset = Subscription.objects.all()
        if device := self.request.query_params.get("device", default=None):
            queryset = queryset.filter(device__uuid=device)
        return queryset

    def perform_create(self, serializer):
        device_uuid = self.request.data["device"]
        topic = self.request.data["topic"]
        topic_arn = sns_client.create_topic(Name=topic)["TopicArn"]
        attributes = {}
        if (group_code := self.request.data["group_code"]) is not None:
            attributes["group_code"] = group_code
        device = Device.objects.get(uuid=device_uuid)
        subscription_arn = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol="application",
            Endpoint=device.endpoint_arn,
            Attributes=attributes,
            ReturnSubscriptionArn=True,
        )["SubscriptionArn"]
        serializer.save(
            device=device,
            topic=topic,
            group_code=group_code,
            subscription_arn=subscription_arn,
        )


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

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return Subscription.objects.get(uuid=uuid)

    def perform_destroy(self, instance):
        if instance.subscription_arn:
            sns_client.unsubscribe(SubscriptionArn=instance.subscription_arn)
        super().perform_destroy(instance)
