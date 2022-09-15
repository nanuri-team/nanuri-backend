from django.urls import path

from . import views

app_name = "nanuri.authentication"

urlpatterns = [
    path(
        "kakao/accounts/",
        views.KakaoAccountCreateAPIView.as_view(),
        name="kakao-account-list",
    ),
    path(
        "token/",
        views.JsonWebTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        views.JsonWebTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "token/verify/",
        views.JsonWebTokenVerifyView.as_view(),
        name="token_verify",
    ),
]
