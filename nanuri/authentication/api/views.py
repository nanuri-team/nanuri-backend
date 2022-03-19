import requests
from django.conf import settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from nanuri.users.models import User


class KakaoTokenAPIView(APIView):
    def get(self, request):
        # 프론트엔드로부터 인가 코드를 받음
        authorization_code = request.GET.get("code", None)
        if authorization_code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 인가 코드를 사용해 액세스 토큰을 발급함
        response = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_REST_API_KEY,
                "redirect_uri": settings.KAKAO_REDIRECT_URI,
                "code": authorization_code,
            },
        )
        access_token = response.json().get("access_token", None)
        if access_token is None:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 액세스 토큰을 카카오 서버에 넘겨서 이메일 정보를 가져옴
        response = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        kakao_account = response.json().get("kakao_account", None)
        if kakao_account is None:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if (
            not kakao_account.get("has_email")
            or not kakao_account.get("is_email_valid")
            or not kakao_account.get("is_email_verified")
        ):
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        email = kakao_account["email"]

        # 이 이메일 정보에 해당하는 유저를 가져옴
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email=email, auth_provider="KAKAO")

        # 토큰을 가져오거나 새로 생성함
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        return Response(data={"token": token.key}, status=status.HTTP_200_OK)
