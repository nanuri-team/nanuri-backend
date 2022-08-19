from django.conf import settings
from drf_spectacular.utils import extend_schema_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from nanuri.aws.sns import sns

from ..models import Device, Subscription
from . import specs
from .serializers import DeviceSerializer, SubscriptionSerializer


@extend_schema_view(**specs.devices_api_specs)
class DeviceCreateAPIView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


@extend_schema_view(**specs.device_api_specs)
class DeviceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return Device.objects.get(uuid=uuid)


@extend_schema_view(**specs.subscriptions_api_specs)
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
        topic_arn = sns.create_topic(Name=topic)["TopicArn"]
        attributes = {}
        if (group_code := self.request.data["group_code"]) is not None:
            attributes["group_code"] = group_code
        device = Device.objects.get(uuid=device_uuid)
        subscription_arn = sns.subscribe(
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


@extend_schema_view(**specs.subscription_api_specs)
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
            sns.unsubscribe(SubscriptionArn=instance.subscription_arn)
        super().perform_destroy(instance)
