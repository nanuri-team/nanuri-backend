from django.urls import path

from . import views

app_name = 'nanuri.authentication'

urlpatterns = [
    path('kakao-token/', views.KakaoTokenAPIView.as_view(), name='token'),
    path('kakao-unlink/', views.KakaoUnlinkAPIView.as_view(), name='unlink'),
]
