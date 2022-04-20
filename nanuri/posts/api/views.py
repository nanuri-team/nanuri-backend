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

from drf_spectacular.utils import OpenApiExample, OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    get=extend_schema(description='<h2>상품 정보를 불러오는 API</h2>', summary='Return all posts', tags=["Post"],),
    post=extend_schema(
        description="""<h2>상품 정보를 등록하는 API</h2>
            <h3>
            - title : 상품 게시글의 제목 <br><br>
            - image : 상품 이미지 파일 등록 <br><br>
            - unit_price : 상품의 가격 <br><br>
            - quantity :  상품의 수량 <br><br>
            - description : 상품에 대한 설명 <br><br>
            - min_participants : 최소 참가 인원 <br><br>
            - max_participants : 최대 참가 인원 <br><br>
            - num_participants : 현재 참가 인원  <br><br>
            - product_url : 상품 URL <br><br>
            - trade_type : 나눔 방법 (DIRECT(직거래), PARCEL(택배 거래)) <br><br>
            - order_status : 상품의 진행상태 (ADVERTISING(인원 모집 중), ORDERING(주문 진행 중), ORDERED(주문 완료), DELIVERING1(1차 배송 중), DELIVERING2(2차 배송 중), DELIVERED(배송 완료), CANCELLED(취소됨)) <br>
            </h3>
        """,  
        summary='Create a new post', 
        tags=["Post"],
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string',
                        'default': '나누리 상품 공동구매 인원 모집합니다.',
                        'required': True,
                        'nullable': False
                    },
                    'image': {
                        'type': 'file',
                        'format': 'formData',
                        'required': False,
                    },
                    'unit_price': {
                        'type': 'integer',
                        'default': '8000',
                        'required': True
                    },
                    'quantity': {
                        'type': 'integer',
                        'default': '6',
                        'required': True
                    },
                    'description': {
                        'type': 'string',
                        'default': '같이 공동구매 하실분?',
                        'required': True
                    },
                    'min_participants': {
                        'type': 'integer',
                        'format': 'Int',
                        'default': '3',
                        'required': True
                    },
                    'max_participants': {
                        'type': 'integer',
                        'format': 'Int',
                        'default': '6',
                        'required': True
                    },
                    'product_url': {
                        'type': 'string',
                        'format': 'url',
                        'default': 'http://localhost:8080/admin/',
                        'required': True
                    },
                    'trade_type': {
                        'type': 'string',
                        'formData': 'enum',
                        'enum': ['DIRECT', 'PARCEL']
                    },
                    'order_status': {
                        'type': 'string',
                        'formData': 'enum',
                        'enum': ['ADVERTISING', 'ORDERING', 'ORDERED', 'DELIVERING1', 'DELIVERING2', 'DELIVERED', 'CANCELLED'],
                        'default': 'ADVERTISING'
                    },
                    'is_published': {
                        'type': 'boolean',
                        'default': 'true'
                    },
                    'view_count': {
                        'type': 'integer',
                        'readOnly': True
                    }
                }
            }
        },
    )
)
class PostListCreateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all().order_by("created_at")
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(writer=self.request.auth.user)


@extend_schema_view(
    get=extend_schema(description='<h2>상품 게시글 정보를 불러오는 API</h2>', summary='Return post by post uuid', tags=["Post"],
    ),
    put=extend_schema(description='<h2>상품 게시글의 전체를 업데이트 하는 API</h2>', summary='Update post', tags=["Post"]),
    patch=extend_schema(description='<h2>상품 게시글을 업데이트 하는 API</h2>', summary='Update post', tags=["Post"]),
    delete=extend_schema(description='<h2>상품 게시글을 삭제하는 API</h2>', summary='Delete post', tags=["Post"])
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


@extend_schema_view(
    get=extend_schema(description='<h2>상품 이미지를 불러오는 API</h2>', summary='Return image', tags=["Post"],),
    post=extend_schema(
        description="""<h2>상품 이미지를 등록하는 API</h2>
            <h3>
            - image : 상품 이미지 파일 등록 <br>
            <h3>
        """,  
        summary='Create post image', 
        tags=["Post"],
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'image': {
                        'type': 'file',
                        'format': 'formData'
                    }
                }
            }
        },
        examples=[
            OpenApiExample(
                name="success_example",
                value={
                    "image": "null",
                },
            ),
        ]
    )
)

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

@extend_schema_view(
    get=extend_schema(description='<h2>상품 게시글의 특정 이미지를 불러오는 API</h2>', summary='Return post by post uuid', tags=["Post"],
    ),
    delete=extend_schema(description='<h2>상품 게시글의 특정 이미지를 삭제하는 API</h2>', summary='Delete post', tags=["Post"])
)
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
