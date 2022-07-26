from rest_framework import serializers

from nanuri.posts.models import Post

from ..models import Device, Subscription


class DeviceSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, many=False, slug_field="email")

    class Meta:
        model = Device
        fields = ["user", "device_token"]


class SubscriptionSerializer(serializers.ModelSerializer):
    device = serializers.SlugRelatedField(read_only=True, many=False, slug_field="uuid")
    post = serializers.SlugRelatedField(
        many=False,
        slug_field="uuid",
        queryset=Post.objects.all(),
    )

    class Meta:
        model = Subscription
        fields = [
            "device",
            "post",
            "receive_chat_messages",
            "receive_comments",
        ]
