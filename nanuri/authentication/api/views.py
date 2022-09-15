import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from ..models import KakaoAccount
from . import exceptions as ex
from . import specs
from .serializers import JsonWebTokenSerializer, KakaoAccountSerializer


def get_kakao_account_info(kakao_id):
    """
    어드민 키를 사용해 카카오 계정 정보를 가져옵니다.

    https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#req-user-info-admin-key
    """
    response = requests.get(
        f"https://kapi.kakao.com/v2/user/me",
        params={"target_id_type": "user_id", "target_id": kakao_id},
        headers={"Authorization": f"KakaoAK {settings.KAKAO_APP_ADMIN_KEY}"},
    )
    if response.status_code != status.HTTP_200_OK:
        raise ex.KakaoAccountRetrieveFailedError(
            detail="카카오 계정 정보를 가져오는데 실패했습니다. 어드민 키가 올바른지 확인해주세요."
        )
    return response.json()


def get_kakao_email(kakao_account_info):
    """
    카카오 이메일 정보를 가져옵니다.

    https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#req-user-info
    """
    if "kakao_account" not in kakao_account_info:
        raise ex.KakaoAccountRetrieveFailedError(
            detail="카카오 계정 정보가 없습니다. 카카오 동의항목에 문제가 발생한 것 같습니다."
        )
    kakao_account = kakao_account_info["kakao_account"]
    if "is_email_valid" not in kakao_account or not kakao_account["is_email_valid"]:
        raise ex.KakaoAccountRetrieveFailedError(detail="이메일이 유효하지 않습니다.")
    if (
        "is_email_verified" not in kakao_account
        or not kakao_account["is_email_verified"]
    ):
        raise ex.KakaoAccountRetrieveFailedError(detail="이메일이 인증되지 않았습니다.")
    if "email" not in kakao_account or not kakao_account["email"]:
        raise ex.KakaoAccountRetrieveFailedError(detail="이메일이 없습니다.")
    return kakao_account["email"]


def get_or_create_user(email):
    """
    유저 객체를 가져오거나 새로 생성합니다.
    """
    user_model = get_user_model()
    try:
        user = user_model.objects.get(email=email)
        user_created = False
    except user_model.DoesNotExist:
        user = user_model.objects.create_user(email=email, auth_provider="KAKAO")
        user_created = True
    return user, user_created


@extend_schema_view(**specs.kakao_accounts_api_specs)
class KakaoAccountCreateAPIView(APIView):
    queryset = KakaoAccount.objects.all()
    serializer_class = KakaoAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            kakao_id = serializer.validated_data["kakao_id"]
            kakao_account_info = get_kakao_account_info(kakao_id)
            email = get_kakao_email(kakao_account_info)
            user, _ = get_or_create_user(email=email)
            try:
                KakaoAccount.objects.get(user=user, kakao_id=kakao_id)
            except KakaoAccount.DoesNotExist:
                serializer.save(user=user, kakao_id=kakao_id)
            refresh = RefreshToken.for_user(user)
            token_serializer = JsonWebTokenSerializer(
                data={
                    "type": "Bearer",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            )
            if token_serializer.is_valid(raise_exception=True):
                return Response(
                    data=token_serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                data=token_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(**specs.jwt_obtain_api_specs)
class JsonWebTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema_view(**specs.jwt_refresh_api_specs)
class JsonWebTokenRefreshView(TokenRefreshView):
    pass


@extend_schema_view(**specs.jwt_verify_api_specs)
class JsonWebTokenVerifyView(TokenVerifyView):
    pass
