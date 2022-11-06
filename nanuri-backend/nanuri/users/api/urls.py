from django.urls import path

from .views import UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView

app_name = "nanuri.users.api"

urlpatterns = [
    path("", UserListCreateAPIView.as_view(), name="list"),
    path("<uuid:uuid>/", UserRetrieveUpdateDestroyAPIView.as_view(), name="detail"),
]
