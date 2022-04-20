from rest_framework import serializers

from ..models import Category, Post, PostImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("image",)


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

    class Meta:
        model = Post
        exclude = ("id",)
        extra_kwargs = {
            "num_participants": {"read_only": True},
            "published_at": {"read_only": True},
            "view_count": {"read_only": True},
            "waited_from": {"read_only": True},
            "waited_until": {"read_only": True},
        }
