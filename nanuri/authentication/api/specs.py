from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)

from .serializers import AuthTokenSerializer

kakao_accounts_api_specs = {
    "post": extend_schema(
        description="<h2>카카오 계정 정보를 등록하는 API</h2>",
        summary="Create a new Kakao user",
        tags=["Kakao Account"],
        responses={
            201: OpenApiResponse(
                response=AuthTokenSerializer,
                description="카카오 계정 생성과 동시에 액세스 토큰과 리프레시 토큰이 발급됩니다.",
            )
        },
    ),
}

jwt_obtain_api_specs = {
    "post": extend_schema(
        description="<h2>JWT를 발급하는 API</h2>",
        summary="Create new JWT",
        tags=["Token"],
        responses={
            200: OpenApiResponse(
                response=TokenObtainPairSerializer,
            )
        },
    ),
}

jwt_refresh_api_specs = {
    "post": extend_schema(
        description="<h2>JWT를 재발급하는 API</h2>",
        summary="Refresh JWT",
        tags=["Token"],
        responses={
            200: OpenApiResponse(
                response=TokenRefreshSerializer,
            )
        },
    )
}


jwt_verify_api_specs = {
    "post": extend_schema(
        description="<h2>JWT를 검증하는 API</h2>",
        summary="Verify JWT",
        tags=["Token"],
        responses={
            200: OpenApiResponse(
                response=TokenVerifySerializer,
            )
        },
    )
}
