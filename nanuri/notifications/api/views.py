from botocore.exceptions import ClientError
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from nanuri.aws.sns import sns

from ..models import Device, Subscription
from . import specs
from .serializers import DeviceSerializer, MessageSerializer, SubscriptionSerializer


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


@extend_schema_view(**specs.subscription_api_specs)
class SubscriptionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return Subscription.objects.get(uuid=uuid)


@extend_schema_view(**specs.messages_api_specs)
class MessageAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            topic = serializer.validated_data["topic"]
            body = serializer.validated_data["body"]
            group_code = serializer.validated_data["group_code"]
            try:
                sns.publish(topic=topic, body=body, group_code=group_code)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ClientError:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
