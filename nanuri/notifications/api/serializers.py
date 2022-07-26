from rest_framework import serializers

from nanuri.posts.models import Post

from ..models import Device, Subscription


class DeviceSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, many=False, slug_field="email")

    class Meta:
        model = Device
        fields = ["user", "device_token", "endpoint_arn"]
        extra_kwargs = {
            "endpoint_arn": {"read_only": True},
        }


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
            "topic",
            "subscription_arn",
        ]
        extra_kwargs = {
            "subscription_arn": {"read_only": True},
        }
