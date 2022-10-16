from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)

from .serializers import AuthTokenSerializer

kakao_accounts_api_specs = {
    "post": extend_schema(
        summary="카카오 계정으로 회원가입 합니다.",
        description="카카오 계정으로 회원가입 합니다.",
        tags=["Authentication"],
        examples=[
            OpenApiExample(
                name="요청 예시",
                description="`kakao_id`는 숫자로 이루어진 카카오 고유 ID입니다. 카카오 SDK를 통해 얻을 수 있습니다. "
                '카카오 로그인 절차에 대한 자세한 설명은 <a href="https://www.notion.so/mingging/baea8a7e3c1d4853ad82561199abba23" target="_blank">이 문서</a>를 참고하세요.',
                value={
                    "kakao_id": 2164473263,
                },
                request_only=True,
            )
        ],
        responses={
            201: OpenApiResponse(
                response=AuthTokenSerializer,
                description="요청이 성공적으로 처리된 경우 새로 생성된 계정의 UUID 값과 토큰 값이 반환됩니다.",
                examples=[
                    OpenApiExample(
                        name="응답 예시",
                        value={
                            "type": "Token",
                            "token": "e52895db38dbf9b90a7fb262bcdcdc2cc8f5d674",
                            "uuid": "93cd4a1e-b5cc-424e-9a54-64a9027fcc1e",
                        },
                        response_only=True,
                        description="현재 발급되는 토큰의 타입은 JWT가 아닌 일반 Token입니다.",
                    ),
                ],
            )
        },
    ),
}

jwt_obtain_api_specs = {
    "post": extend_schema(
        summary="JWT를 발급합니다.",
        description="JWT를 발급합니다.",
        tags=["Token"],
        examples=[
            OpenApiExample(
                name="요청 예시",
                value={
                    "email": "user@example.com",
                    "password": "password",
                },
                request_only=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=TokenObtainPairSerializer,
                description="요청이 성공적으로 처리된 경우 새로운 액세스 토큰과 리프레시 토큰이 발급됩니다.",
                examples=[
                    OpenApiExample(
                        name="응답 예시",
                        value={
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1OTEwNTA0LCJpYXQiOjE2NjU5MTAyMDQsImp0aSI6IjYwY2M2NDk0ZmIyYjRkYzdiYjlmMWYzYzRhYzg3MWE2IiwidXNlcl9pZCI6Mn0.kNkXW930_L87vwxlLjzpV1SNxs7wYZVNwuM6iAeOizk",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NTk5NjYwNCwiaWF0IjoxNjY1OTEwMjA0LCJqdGkiOiJmNWViNjg0MzE1YWM0Nzg5ODk4YTA0OThlMDNhMjQxNSIsInVzZXJfaWQiOjJ9.tjLyyNBC4Ph_XMRslznUTPCqsYTlDmNq573Y_SRqmmE",
                        },
                        response_only=True,
                        description="새로 발급한 JWT 액세스 토큰의 유효기간은 5분, JWT 리프레시 토큰의 유효기간은 1일입니다.",
                    )
                ],
            )
        },
    ),
}

jwt_refresh_api_specs = {
    "post": extend_schema(
        summary="JWT 액세스 토큰을 재발급합니다.",
        description="JWT 액세스 토큰을 재발급합니다.",
        tags=["Token"],
        examples=[
            OpenApiExample(
                name="요청 예시",
                value={
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NTk5NjYwNCwiaWF0IjoxNjY1OTEwMjA0LCJqdGkiOiJmNWViNjg0MzE1YWM0Nzg5ODk4YTA0OThlMDNhMjQxNSIsInVzZXJfaWQiOjJ9.tjLyyNBC4Ph_XMRslznUTPCqsYTlDmNq573Y_SRqmmE",
                },
                request_only=True,
                description="이전에 발급 받았던 JWT 리프레시 토큰을 입력하세요.",
            )
        ],
        responses={
            200: OpenApiResponse(
                response=TokenRefreshSerializer,
                description="전달한 JWT 리프레시 토큰이 유효한 경우, 새로운 JWT 액세스 토큰이 생성되어 반환됩니다.",
                examples=[
                    OpenApiExample(
                        name="응답 예시",
                        value={
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1OTE1Nzc3LCJpYXQiOjE2NjU5MTUxNzcsImp0aSI6ImIyYmFiOTVlZmRkYjQzMmFhZjRlYzk2MTRiOTlmM2EwIiwidXNlcl9pZCI6MX0.im3of1AQ1DiUxOqFRzr664E3jvKcTX_b0hRayNvq0d0",
                        },
                        response_only=True,
                    )
                ],
            ),
            401: OpenApiResponse(
                response=inline_serializer(
                    name="error",
                    fields={
                        "code": serializers.CharField(default="token_not_valid"),
                        "detail": serializers.CharField(
                            default="Token 'exp' claim has expired"
                        ),
                    },
                ),
                description="주어진 JWT 리프레시 토큰이 만료된 경우, 401 상태 코드와 함께 에러 정보가 담긴 JSON 데이터가 반환됩니다.",
            ),
        },
    )
}


jwt_verify_api_specs = {
    "post": extend_schema(
        summary="JWT 액세스 토큰을 검증합니다.",
        description="JWT 액세스 토큰을 검증합니다.",
        tags=["Token"],
        examples=[
            OpenApiExample(
                name="요청 예시",
                value={
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1OTEwNTA0LCJpYXQiOjE2NjU5MTAyMDQsImp0aSI6IjYwY2M2NDk0ZmIyYjRkYzdiYjlmMWYzYzRhYzg3MWE2IiwidXNlcl9pZCI6Mn0.kNkXW930_L87vwxlLjzpV1SNxs7wYZVNwuM6iAeOizk",
                },
                description="이전에 발급 받았던 JWT 액세스 토큰 값을 입력하세요.",
                request_only=True,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=TokenVerifySerializer,
                description="주어진 JWT 액세스 토큰이 유효한 경우, 200 상태 코드와 함께 빈 JSON 데이터가 반환됩니다.",
                examples=[
                    OpenApiExample(
                        name="응답 예시",
                        value=dict(),
                        response_only=True,
                    )
                ],
            ),
            401: OpenApiResponse(
                response=inline_serializer(
                    name="error",
                    fields={
                        "code": serializers.CharField(default="token_not_valid"),
                        "detail": serializers.CharField(
                            default="Token 'exp' claim has expired"
                        ),
                    },
                ),
                description="주어진 JWT 액세스 토큰이 만료된 경우, 401 상태 코드와 함께 에러 정보가 담긴 JSON 데이터가 반환됩니다.",
            ),
        },
    )
}
