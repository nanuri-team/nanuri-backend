from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if "password" in validated_data:
            instance.set_password(validated_data['password'])
        return instance

    class Meta:
        model = User
        exclude = ('id', 'favorite_posts')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
            },
            'last_login': {'read_only': True},
        }
