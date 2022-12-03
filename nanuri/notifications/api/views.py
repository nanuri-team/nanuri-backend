from botocore.exceptions import ClientError
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from nanuri.aws.sns import sns
from .serializers import DeviceSerializer, MessageSerializer, SubscriptionSerializer
from ..models import Device, Subscription


class DeviceCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class DeviceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return Device.objects.get(uuid=uuid)


class SubscriptionListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        queryset = Subscription.objects.all()
        if device := self.request.query_params.get("device", default=None):
            queryset = queryset.filter(device__uuid=device)
        return queryset


class SubscriptionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return Subscription.objects.get(uuid=uuid)


class MessageAPIView(APIView):
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
