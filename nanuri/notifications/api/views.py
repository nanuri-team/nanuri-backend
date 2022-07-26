from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from nanuri.posts.models import Post

from ..models import Device, Subscription
from .serializers import DeviceSerializer, SubscriptionSerializer


class DeviceCreateAPIView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


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
        serializer.save(device=device, post=post)


class SubscriptionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
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
