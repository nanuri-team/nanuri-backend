from rest_framework import serializers

from nanuri.users.api.serializers import UserSerializer

from ..models import Comment, Post, SubComment


class PostSerializer(serializers.ModelSerializer):
    writer = UserSerializer(many=False, read_only=True)

    participants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="email",
    )
    favored_by = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="email",
    )
    images = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="image_url",
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
        slug_field="uuid",
        queryset=Post.objects.all(),
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
        slug_field="uuid",
        queryset=Comment.objects.all(),
    )
    writer = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email",
    )

    class Meta:
        model = SubComment
        exclude = ("id",)
