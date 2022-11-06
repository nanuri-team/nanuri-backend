from rest_framework import serializers

from nanuri.users.api.serializers import UserSerializer

from ..models import Comment, Post, SubComment


class PostSerializer(serializers.ModelSerializer):
    writer = UserSerializer(many=False, read_only=True)
    distance = serializers.CharField(max_length=255, read_only=True)

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
        fields = (
            "uuid",
            "title",
            "category",
            "image",
            "unit_price",
            "quantity",
            "description",
            "min_participants",
            "max_participants",
            "num_participants",
            "product_url",
            "trade_type",
            "order_status",
            "is_published",
            "published_at",
            "view_count",
            "waited_from",
            "waited_until",
            "created_at",
            "updated_at",
            "writer",
            "distance",
            "participants",
            "favored_by",
            "images",
        )
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
        fields = (
            "uuid",
            "post",
            "text",
            "writer",
            "created_at",
            "updated_at",
        )


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
        fields = (
            "uuid",
            "comment",
            "text",
            "writer",
            "created_at",
            "updated_at",
        )
