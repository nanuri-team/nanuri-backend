import requests
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from nanuri.users.models import User

from . import exceptions as ex


def get_code_query_param(request):
    """
    요청의 쿼리 파라미터에서 인가 코드 정보를 추출합니다.
    """
    authorization_code = request.GET.get("code", None)
    if authorization_code is None:
        raise ex.KakaoAuthorizationCodeInvalidError()
    return authorization_code


def refresh_kakao_token(authorization_code):
    """
    인가 코드를 사용해 카카오 토큰을 (재)발급합니다.

    https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#refresh-token
    """
    response = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_REST_API_KEY,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "code": authorization_code,
        },
    )
    if response.status_code != status.HTTP_200_OK:
        raise ex.KakaoTokenRefreshFailedError()
    return response.json()


def get_kakao_account_info(access_token):
    """
    카카오 계정 정보를 가져옵니다.

    https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#req-user-info
    """
    response = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != status.HTTP_200_OK:
        raise ex.KakaoAccountRetrieveFailedError(
            detail="카카오 계정 정보를 가져오는데 실패했습니다. 액세스 토큰이 올바른지 확인해주세요."
        )
    return response.json()


def get_kakao_email(access_token):
    """
    카카오 이메일 정보를 가져옵니다.

    https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#req-user-info
    """
    kakao_account_info = get_kakao_account_info(access_token)
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
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(email=email, auth_provider="KAKAO")
    return user


def get_or_create_token(user):
    """
    토큰 객체를 가져오거나 새로 생성합니다.
    """
    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)
    return token


class KakaoTokenAPIView(APIView):
    def get(self, request):
        authorization_code = get_code_query_param(request)
        access_token = refresh_kakao_token(authorization_code)["access_token"]
        email = get_kakao_email(access_token)
        user = get_or_create_user(email)
        token = get_or_create_token(user)
        return Response(data={"token": token.key}, status=status.HTTP_200_OK)
