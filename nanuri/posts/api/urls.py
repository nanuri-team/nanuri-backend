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
        "comments/",
        views.CommentListCreateAPIView.as_view(),
        name="comment-list",
    ),
    path(
        "comments/<uuid:uuid>/",
        views.CommentRetrieveUpdateDestroyAPIView.as_view(),
        name="comment-detail",
    ),
    path(
        "sub-comments/",
        views.SubCommentListCreateAPIView.as_view(),
        name="sub-comment-list",
    ),
    path(
        "sub-comments/<uuid:uuid>/",
        views.SubCommentRetrieveUpdateDestroyAPIView.as_view(),
        name="sub-comment-detail",
    ),
]
