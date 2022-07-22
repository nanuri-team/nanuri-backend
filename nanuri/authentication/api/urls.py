from django.urls import path

from . import views

app_name = "nanuri.authentication"

urlpatterns = [
    path(
        "kakao/accounts/",
        views.KakaoAccountCreateAPIView.as_view(),
        name="kakao-account-list",
    ),
]
