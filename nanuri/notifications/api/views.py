import boto3
from django.conf import settings
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


class DeviceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
    lookup_field = "uuid"


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
