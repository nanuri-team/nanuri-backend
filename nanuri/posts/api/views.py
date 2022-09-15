from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.core.files.storage import default_storage
from django.db.models import F
from drf_spectacular.utils import extend_schema_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from ..models import Comment, Post, PostImage, SubComment
from . import specs
from .serializers import CommentSerializer, PostSerializer, SubCommentSerializer


@extend_schema_view(**specs.posts_api_specs)
class PostListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Post.objects.all()
        if user := self.request.query_params.get("user", default=None):
            queryset = queryset.filter(writer__uuid=user)

        distance = self.request.query_params.get("distance", default=None)
        if distance:
            queryset = (
                queryset.annotate(
                    distance=Distance(F("writer__location"), self.request.user.location)
                )
                .order_by("distance")
                .filter(distance__lt=D(m=distance))
            )

        return queryset

    def perform_create(self, serializer):
        writer = self.request.user
        post = serializer.save(writer=writer)
        post_images = [
            PostImage(post=post, image=image_file)
            for image_file in self.request.FILES.getlist("images")
        ]
        PostImage.objects.bulk_create(post_images)
        post.participants.add(writer)


@extend_schema_view(**specs.post_api_specs)
class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "uuid"

    def perform_destroy(self, instance):
        for post_image in instance.images.all():
            default_storage.delete(post_image.image.name)
        default_storage.delete(instance.image.name)
        super().perform_destroy(instance)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        uuid = self.kwargs[self.lookup_field]
        post = Post.objects.get(uuid=uuid)
        post_images = post.images.all()
        for post_image in post_images:
            default_storage.delete(post_image.image.name)
            post_image.delete()
        new_post_images = [
            PostImage(post=post, image=image_file)
            for image_file in self.request.FILES.getlist("images")
        ]
        PostImage.objects.bulk_create(new_post_images)


@extend_schema_view(**specs.comments_api_specs)
class CommentListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Comment.objects.all()
        if post := self.request.query_params.get("post", default=None):
            queryset = queryset.filter(post__uuid=post)
        return queryset

    def perform_create(self, serializer):
        post_uuid = self.request.data["post"]
        post = Post.objects.get(uuid=post_uuid)
        writer = self.request.user
        serializer.save(post=post, writer=writer)


@extend_schema_view(**specs.comment_api_specs)
class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return Comment.objects.get(uuid=uuid)


@extend_schema_view(**specs.sub_comments_api_specs)
class SubCommentListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubCommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = SubComment.objects.all()
        if comment := self.request.query_params.get("comment", default=None):
            queryset = queryset.filter(comment__uuid=comment)
        return queryset

    def perform_create(self, serializer):
        comment_uuid = self.request.data["comment"]
        comment = Comment.objects.get(uuid=comment_uuid)
        writer = self.request.user
        serializer.save(comment=comment, writer=writer)


@extend_schema_view(**specs.sub_comment_api_specs)
class SubCommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubCommentSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return SubComment.objects.get(uuid=uuid)
