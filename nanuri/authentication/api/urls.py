from django.urls import path

from . import views

app_name = 'nanuri.authentication'

urlpatterns = [
    path(
        'kakao/token/callback/',
        views.KakaoTokenCallbackAPIView.as_view(),
        name='token_callback',
    ),
    path(
        'kakao/unlink/',
        views.KakaoUnlinkAPIView.as_view(),
        name='unlink',
    ),
]
