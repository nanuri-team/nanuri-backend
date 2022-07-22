from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="uuid",
    )
    favorite_posts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="uuid",
    )

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        return instance

    class Meta:
        model = User
        exclude = ("id",)
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
            },
            "last_login": {"read_only": True},
        }
