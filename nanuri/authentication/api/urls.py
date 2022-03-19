from django.urls import path

from .views import KakaoTokenAPIView

app_name = 'nanuri.authentication'

urlpatterns = [
    path('kakao-token/', KakaoTokenAPIView.as_view(), name='token'),
]
