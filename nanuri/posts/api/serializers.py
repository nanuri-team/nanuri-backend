from rest_framework import serializers

from ..models import Category, Order, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class PostSerializer(serializers.ModelSerializer):
    writer = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email",
    )
    participants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="email",
    )
    category = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name",
    )
    favored_by = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="email",
    )
    orders = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="uuid",
    )

    class Meta:
        model = Post
        exclude = ("id",)
        extra_kwargs = {
            'num_participants': {'read_only': True},
            'published_at': {'read_only': True},
            'participants': {'read_only': True},
        }


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ("id",)
