from rest_framework import status
from rest_framework.exceptions import APIException


class KakaoAuthorizationCodeInvalidError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "카카오 인가 코드가 없거나 유효하지 않습니다."
    default_code = "kakao_authorization_code_invalid"


class KakaoTokenRefreshFailedError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "카카오 토큰 정보가 없거나 유효하지 않습니다. 카카오 REST API Key, Redirect URI, 인가 코드가 올바른지 확인하세요."
    default_code = "kakao_token_refresh_failed"


class KakaoAccountRetrieveFailedError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "카카오 계정 정보를 가져올 수 없습니다. 카카오 토큰 정보가 올바른지 확인하세요."
    default_code = "kakao_account_retrieve_failed"


class KakaoAccountUnlinkFailedError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "카카오 계정 연결 끊기에 실패했습니다."
    default_code = "kakao_account_unlink_failed"


class KakaoAccountAlreadyUnlinkedError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 연결이 끊어진 카카오 계정입니다."
    default_code = "kakao_account_already_unlinked"
