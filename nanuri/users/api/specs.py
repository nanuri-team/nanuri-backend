from drf_spectacular.utils import OpenApiExample, extend_schema

users_api_specs = {
    "get": extend_schema(
        description="<h2>회원 정보를 불러오는 API</h2>",
        summary="Return all users",
        tags=["User"],
    ),
    "post": extend_schema(
        description="<h2>회원 정보를 등록하는 API</h2>",
        summary="Create a new user",
        tags=["User"],
        examples=[
            OpenApiExample(
                name="example_all_fields",
                value={
                    "email": "michaelmontoya@example.com",
                    "password": "uG5*(GNr&F",
                    "nickname": "michael",
                    "is_active": True,
                    "is_admin": False,
                    "address": "9197 Turner Roads\nNorth Melissaberg, MT 83503",
                    "profile": "https://dummyimage.com/2x721.jpeg",
                    "auth_provider": "KAKAO",
                    "location": "SRID=4326;POINT (-22.86 1.2281245)",
                },
                description="location 포맷은 `SRID=4326;POINT (경도 위도)`입니다.",
            ),
            OpenApiExample(
                name="example_required_fields_only",
                value={
                    "email": "michaelmontoya@example.com",
                    "password": "uG5*(GNr&F",
                },
            ),
        ],
    ),
}


user_api_specs = {
    "get": extend_schema(
        description="<h2>회원 정보를 불러오는 API</h2>",
        summary="Return user by user uuid",
        tags=["User"],
    ),
    "put": extend_schema(
        description="<h2>회원 정보 전체를 업데이트 하는 API</h2>",
        summary="Update user",
        tags=["User"],
        examples=[
            OpenApiExample(
                name="success_example",
                value={
                    "email": "michaelmontoya@example.com",
                    "password": "uG5*(GNr&F",
                    "nickname": "michael",
                    "is_active": True,
                    "is_admin": False,
                    "address": "9197 Turner Roads\nNorth Melissaberg, MT 83503",
                    "profile": "https://dummyimage.com/2x721.jpeg",
                    "auth_provider": "KAKAO",
                    "location": "SRID=4326;POINT (-22.86 1.2281245)",
                },
            ),
        ],
    ),
    "patch": extend_schema(
        description="<h2>회원 정보를 부분 수정하는 API</h2>",
        summary="Update user",
        tags=["User"],
        examples=[
            OpenApiExample(
                name="success_example",
                value={
                    "location": "SRID=4326;POINT (-22.86 1.2281245)",
                },
            ),
        ],
    ),
    "delete": extend_schema(
        description="<h2>회원 정보를 삭제하는 API</h2>",
        summary="Delete user",
        tags=["User"],
    ),
}
