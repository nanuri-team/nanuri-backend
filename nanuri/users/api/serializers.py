from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        return instance

    class Meta:
        model = User
        exclude = ('id',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
            },
            'last_login': {'read_only': True},
        }
