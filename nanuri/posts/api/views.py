from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.core.files.storage import default_storage
from django.db.models import F
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import CommentSerializer, PostSerializer, SubCommentSerializer
from ..models import Comment, Post, PostImage, SubComment


class PostListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()

        if location := self.request.user.location:
            queryset = queryset.annotate(
                distance=Distance(F("writer__location"), location)
            )

        if user := self.request.query_params.get("user"):
            queryset = queryset.filter(writer__uuid=user)

        if distance := self.request.query_params.get("distance"):
            queryset = queryset.filter(distance__lt=D(m=distance)).order_by("distance")

        if categories := self.request.query_params.getlist("category"):
            queryset = queryset.filter(category__in=categories)

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


class CommentListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

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


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return Comment.objects.get(uuid=uuid)


class SubCommentListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubCommentSerializer

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


class SubCommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubCommentSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return SubComment.objects.get(uuid=uuid)
