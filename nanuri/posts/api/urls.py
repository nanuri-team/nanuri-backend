from django.urls import path

from . import views

app_name = "nanuri.posts.api"

urlpatterns = [
    path(
        "",
        views.PostListCreateAPIView.as_view(),
        name="list",
    ),
    path(
        "<uuid:uuid>/",
        views.PostRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:uuid>/images/",
        views.PostImageListCreateAPIView.as_view(),
        name="image-list",
    ),
    path(
        "<uuid:uuid>/images/<str:filename>/",
        views.PostImageRetrieveDestroyAPIView.as_view(),
        name="image-detail",
    ),
]
