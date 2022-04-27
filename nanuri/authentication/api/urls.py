from django.urls import path

from . import views

app_name = 'nanuri.authentication'

urlpatterns = [
    path(
        'kakao/token/callback/',
        views.KakaoTokenCallbackAPIView.as_view(),
        name='kakao-token_callback',
    ),
    path(
        'kakao/unlink/',
        views.KakaoUnlinkAPIView.as_view(),
        name='kakao-unlink',
    ),
    path(
        'kakao/accounts/',
        views.KakaoAccountListCreateAPIView.as_view(),
        name='kakao-account-list',
    ),
    path(
        'kakao/accounts/<int:kakao_id>/',
        views.KakaoAccountRetrieveDestroyAPIView.as_view(),
        name='kakao-account-detail',
    ),
]
