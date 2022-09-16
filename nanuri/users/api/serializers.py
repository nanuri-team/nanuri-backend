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

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            "uuid",
            "email",
            "password",
            "nickname",
            "is_active",
            "is_admin",
            "last_login",
            "address",
            "profile",
            "auth_provider",
            "location",
            "posts",
            "favorite_posts",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
            },
            "last_login": {"read_only": True},
        }
