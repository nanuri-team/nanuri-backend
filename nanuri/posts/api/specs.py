from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

posts_api_specs = {
    "get": extend_schema(
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
    "post": extend_schema(
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
}


post_api_specs = {
    "get": extend_schema(
        description="<h2>상품 게시글 정보를 불러오는 API</h2>",
        summary="Return post by post uuid",
        tags=["Post"],
    ),
    "put": extend_schema(
        description="<h2>상품 게시글의 전체를 업데이트 하는 API</h2>",
        summary="Update post",
        tags=["Post"],
    ),
    "patch": extend_schema(
        description="<h2>상품 게시글을 업데이트 하는 API</h2>",
        summary="Update post",
        tags=["Post"],
    ),
    "delete": extend_schema(
        description="<h2>상품 게시글을 삭제하는 API</h2>",
        summary="Delete post",
        tags=["Post"],
    ),
}


comments_api_specs = {
    "get": extend_schema(
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
    "post": extend_schema(
        description="<h2>상품 댓글을 등록하는 API</h2>",
        summary="Create a new comment",
        tags=["Comment"],
    ),
}


comment_api_specs = {
    "get": extend_schema(
        description="<h2>특정 댓글을 조회하는 API</h2>",
        summary="Get a comment by comment UUID",
        tags=["Comment"],
    ),
    "put": extend_schema(
        description="<h2>특정 댓글을 수정하는 API</h2>",
        summary="Update a comment",
        tags=["Comment"],
    ),
    "patch": extend_schema(
        description="<h2>특정 댓글을 부분 수정하는 API</h2>",
        summary="Patch a comment",
        tags=["Comment"],
    ),
    "delete": extend_schema(
        description="<h2>특정 댓글을 삭제하는 API</h2>",
        summary="Delete a comment",
        tags=["Comment"],
    ),
}


sub_comments_api_specs = {
    "get": extend_schema(
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
    "post": extend_schema(
        description="<h2>대댓글을 생성하는 API</h2>",
        summary="Create a new sub comment",
        tags=["Sub Comment"],
    ),
}


sub_comment_api_specs = {
    "get": extend_schema(
        description="<h2>특정 대댓글을 조회하는 API</h2>",
        summary="Get a sub comment",
        tags=["Sub Comment"],
    ),
    "put": extend_schema(
        description="<h2>특정 대댓글을 수정하는 API</h2>",
        summary="Update a sub comment",
        tags=["Sub Comment"],
    ),
    "patch": extend_schema(
        description="<h2>특정 대댓글을 부분 수정하는 API</h2>",
        summary="Patch a sub comment",
        tags=["Sub Comment"],
    ),
    "delete": extend_schema(
        description="<h2>특정 대댓글을 삭제하는 API</h2>",
        summary="Remove a sub comment",
        tags=["Sub Comment"],
    ),
}
