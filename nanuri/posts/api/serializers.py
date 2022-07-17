from rest_framework import serializers

from ..models import Category, Comment, Post, PostImage, SubComment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        exclude = ("id",)


class PostSerializer(serializers.ModelSerializer):
    writer = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email",
    )

    writer_address = serializers.StringRelatedField(source="writer.address", read_only=True, many=False)
    writer_nickname = serializers.StringRelatedField(source="writer.nickname", read_only=True, many=False)

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
        }


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="uuid",
    )
    writer = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email",
    )

    class Meta:
        model = Comment
        exclude = ("id",)


class SubCommentSerializer(serializers.ModelSerializer):
    comment = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="uuid",
    )
    writer = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email",
    )

    class Meta:
        model = SubComment
        exclude = ("id",)
