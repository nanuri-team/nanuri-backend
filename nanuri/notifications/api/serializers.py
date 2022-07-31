from rest_framework import serializers

from ..models import Device, Subscription


class DeviceSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, many=False, slug_field="email")

    class Meta:
        model = Device
        fields = ["uuid", "user", "device_token", "endpoint_arn", "opt_in"]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "endpoint_arn": {"read_only": True},
        }


class SubscriptionSerializer(serializers.ModelSerializer):
    device = serializers.SlugRelatedField(
        many=False,
        slug_field="uuid",
        queryset=Device.objects.all(),
    )

    class Meta:
        model = Subscription
        fields = [
            "uuid",
            "device",
            "topic",
            "group_code",
            "opt_in",
            "subscription_arn",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "subscription_arn": {"read_only": True},
        }
