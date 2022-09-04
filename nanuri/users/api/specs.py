from drf_spectacular.utils import OpenApiExample, extend_schema

users_api_specs = {
    "get": extend_schema(
        description="<h2>회원 정보를 불러오는 API</h2>",
        summary="Return all users",
        tags=["User"],
    ),
    "post": extend_schema(
        description="""<h2>회원 정보를 등록하는 API</h2>
            <h3>
            - email : 사용자의 email <br><br>
            - nickname : 사용자의 닉네임 <br><br>
            - is_active : 계정의 활성화 유무 <br><br>
            - is_admin :  admin 권한 제공 유무 <br><br>
            - address : 사용자의 주소 <br><br>
            - profile_url : 사용자의 프로필 이미지 url  <br><br>
            - auth_provider : 소셜로그인 종류 (APPLE, KAKAO) <br><br>
            </h3>
        """,
        summary="Create a new user",
        tags=["User"],
        examples=[
            OpenApiExample(
                name="success_example",
                value={
                    "password": "null",
                    "email": "nanuri@example.com",
                    "nickname": "nanuri",
                    "is_active": "true",
                    "is_admin": "false",
                    "address": "나누리시 나누리구 나누리동",
                    "profile_url": "https://nanuri.app/",
                    "auth_provider": "APPLE",
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
        description="""<h2>회원 정보 전체를 업데이트 하는 API</h2>
            ! 전체 필드에 대해서 update
            <h3>
            - email : 사용자의 email <br><br>
            - nickname : 사용자의 닉네임 <br><br>
            - is_active : 계정의 활성화 유무 <br><br>
            - is_admin :  admin 권한 제공 유무 <br><br>
            - address : 사용자의 주소 <br><br>
            - profile_url : 사용자의 프로필 이미지 url  <br><br>
            - auth_provider : 소셜로그인 종류 (APPLE, KAKAO) <br><br>
            </h3>
        """,
        summary="Update user",
        tags=["User"],
        examples=[
            OpenApiExample(
                name="success_example",
                value={
                    "password": "null",
                    "email": "nanuri@example.com",
                    "nickname": "nanuri",
                    "is_active": "true",
                    "is_admin": "false",
                    "address": "나누리시 나누리구 나누리동",
                    "profile_url": "https://nanuri.app/",
                    "auth_provider": "APPLE",
                },
            ),
        ],
    ),
    "patch": extend_schema(
        description="""<h2>회원 정보를 업데이트 하는 API</h2>
            ! 필요한 필드만 update
            <h3>
            - email : 사용자의 email <br><br>
            - nickname : 사용자의 닉네임 <br><br>
            - is_active : 계정의 활성화 유무 <br><br>
            - is_admin :  admin 권한 제공 유무 <br><br>
            - address : 사용자의 주소 <br><br>
            - profile_url : 사용자의 프로필 이미지 url  <br><br>
            - auth_provider : 소셜로그인 종류 (APPLE, KAKAO) <br><br>
            </h3>
        """,
        summary="Update user",
        tags=["User"],
        examples=[
            OpenApiExample(
                name="success_example",
                value={
                    "password": "null",
                    "email": "nanuri@example.com",
                    "nickname": "nanuri",
                    "is_active": "true",
                    "is_admin": "false",
                    "address": "나누리시 나누리구 나누리동",
                    "profile_url": "https://nanuri.app/",
                    "auth_provider": "APPLE",
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
