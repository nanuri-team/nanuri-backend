from django.core.files.storage import default_storage
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from ..models import Post, PostImage
from .serializers import PostImageSerializer, PostSerializer


class PostListCreateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all().order_by("created_at")
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "uuid"

    def perform_destroy(self, instance):
        for post_image in instance.images.all():
            default_storage.delete(post_image.image.name)
        default_storage.delete(instance.image.name)
        super().perform_destroy(instance)


class PostImageListCreateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostImageSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        uuid = self.kwargs["uuid"]
        return PostImage.objects.filter(post__uuid=uuid)

    def perform_create(self, serializer):
        uuid = self.request.parser_context["kwargs"]["uuid"]
        post = Post.objects.get(uuid=uuid)
        serializer.save(post=post)


class PostImageRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostImageSerializer
    lookup_url_kwarg = "filename"

    def get_queryset(self):
        uuid = self.kwargs["uuid"]
        return PostImage.objects.filter(post__uuid=uuid)

    def get_object(self):
        queryset = self.get_queryset()
        filename = self.kwargs[self.lookup_url_kwarg]
        obj = queryset.get(image__endswith=filename)
        return obj

    def perform_destroy(self, instance):
        default_storage.delete(instance.image.name)
        super().perform_destroy(instance)
