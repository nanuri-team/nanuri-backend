from django.core.files.storage import default_storage
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from ..models import Comment, Post, PostImage, SubComment
from .serializers import CommentSerializer, PostSerializer, SubCommentSerializer


@extend_schema_view(
    get=extend_schema(
        description="<h2>상품 정보를 불러오는 API</h2>",
        summary="Return all posts",
        tags=["Post"],
        parameters=[
            OpenApiParameter(
                name="user",
                location=OpenApiParameter.QUERY,
                description="User UUID",
                required=False,
                type=str,
            )
        ],
    ),
    post=extend_schema(
        description="<h2>글을 생성하는 API</h2>",
        summary="Create a new post",
        tags=["Post"],
        examples=[
            OpenApiExample(
                name="Request #1",
                value={
                    "title": "콜라 공동구매합니다",
                    "unit_price": 1500,
                    "quantity": 30,
                    "description": "좋은 가격에 콜라 같이 구매하실 분~",
                    "min_participants": 10,
                    "max_participants": 50,
                    "product_url": "https://example.com/items/coke",
                    "category": "FOOD",
                    "trade_type": "DIRECT",
                    "waited_until": "2022-08-05",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Response #1",
                value={
                    "writer": "nanuri@nanuri.app",
                    "writer_address": "나누리시 나누리구 나누리동 나누리아파트 101동 101호",
                    "writer_nickname": "나누리",
                    "participants": ["nanuri@nanuri.app"],
                    "favored_by": [],
                    "images": [],
                    "uuid": "b6accf2d-f527-4096-bcf2-3a18198db198",
                    "title": "콜라 공동구매합니다",
                    "image": None,
                    "unit_price": 1500,
                    "quantity": 30,
                    "description": "좋은 가격에 콜라 같이 구매하실 분~",
                    "category": "FOOD",
                    "min_participants": 10,
                    "max_participants": 50,
                    "num_participants": 0,
                    "product_url": "https://nanuri.app/items/coke",
                    "trade_type": "DIRECT",
                    "order_status": "WAITING",
                    "is_published": True,
                    "published_at": "2022-08-02T13:13:08.095902Z",
                    "view_count": 0,
                    "waited_from": "2022-08-02",
                    "waited_until": "2022-08-05",
                    "created_at": "2022-08-02T13:13:08.309620Z",
                    "updated_at": "2022-08-02T13:13:08.309642Z",
                },
                response_only=True,
            ),
        ],
    ),
)
class PostListCreateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Post.objects.all()
        if user := self.request.query_params.get("user", default=None):
            queryset = queryset.filter(writer__uuid=user)
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


@extend_schema_view(
    get=extend_schema(
        description="<h2>상품 게시글 정보를 불러오는 API</h2>",
        summary="Return post by post uuid",
        tags=["Post"],
    ),
    put=extend_schema(
        description="<h2>상품 게시글의 전체를 업데이트 하는 API</h2>",
        summary="Update post",
        tags=["Post"],
    ),
    patch=extend_schema(
        description="<h2>상품 게시글을 업데이트 하는 API</h2>",
        summary="Update post",
        tags=["Post"],
    ),
    delete=extend_schema(
        description="<h2>상품 게시글을 삭제하는 API</h2>",
        summary="Delete post",
        tags=["Post"],
    ),
)
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


@extend_schema_view(
    get=extend_schema(
        description="<h2>댓글 목록을 조회하는 API</h2>",
        summary="Get list of comments",
        tags=["Comment"],
        parameters=[
            OpenApiParameter(
                name="post",
                location=OpenApiParameter.QUERY,
                description="Post UUID",
                required=False,
                type=str,
            )
        ],
    ),
    post=extend_schema(
        description="<h2>상품 댓글을 등록하는 API</h2>",
        summary="Create a new comment",
        tags=["Comment"],
    ),
)
class CommentListCreateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
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


@extend_schema_view(
    get=extend_schema(
        description="<h2>특정 댓글을 조회하는 API</h2>",
        summary="Get a comment by comment UUID",
        tags=["Comment"],
    ),
    put=extend_schema(
        description="<h2>특정 댓글을 수정하는 API</h2>",
        summary="Update a comment",
        tags=["Comment"],
    ),
    patch=extend_schema(
        description="<h2>특정 댓글을 부분 수정하는 API</h2>",
        summary="Patch a comment",
        tags=["Comment"],
    ),
    delete=extend_schema(
        description="<h2>특정 댓글을 삭제하는 API</h2>",
        summary="Delete a comment",
        tags=["Comment"],
    ),
)
class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return Comment.objects.get(uuid=uuid)


@extend_schema_view(
    get=extend_schema(
        description="<h2>대댓글 목록을 조회하는 API</h2>",
        summary="Get list of sub comments",
        tags=["Sub Comment"],
        parameters=[
            OpenApiParameter(
                name="comment",
                location=OpenApiParameter.QUERY,
                description="Comment UUID",
                required=False,
                type=str,
            )
        ],
    ),
    post=extend_schema(
        description="<h2>대댓글을 생성하는 API</h2>",
        summary="Create a new sub comment",
        tags=["Sub Comment"],
    ),
)
class SubCommentListCreateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
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


@extend_schema_view(
    get=extend_schema(
        description="<h2>특정 대댓글을 조회하는 API</h2>",
        summary="Get a sub comment",
        tags=["Sub Comment"],
    ),
    put=extend_schema(
        description="<h2>특정 대댓글을 수정하는 API</h2>",
        summary="Update a sub comment",
        tags=["Sub Comment"],
    ),
    patch=extend_schema(
        description="<h2>특정 대댓글을 부분 수정하는 API</h2>",
        summary="Patch a sub comment",
        tags=["Sub Comment"],
    ),
    delete=extend_schema(
        description="<h2>특정 대댓글을 삭제하는 API</h2>",
        summary="Remove a sub comment",
        tags=["Sub Comment"],
    ),
)
class SubCommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubCommentSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs[self.lookup_field]
        return SubComment.objects.get(uuid=uuid)
