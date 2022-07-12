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
    path(
        "<uuid:uuid>/comments/",
        views.CommentListCreateAPIView.as_view(),
        name="comment-list",
    ),
    path(
        "<uuid:uuid>/comments/<uuid:comment_uuid>/",
        views.CommentRetrieveUpdateDestroyAPIView.as_view(),
        name="comment-detail",
    ),
    path(
        "<uuid:uuid>/comments/<uuid:comment_uuid>/sub-comments/",
        views.SubCommentListCreateAPIView.as_view(),
        name="sub-comment-list",
    ),
    path(
        "<uuid:uuid>/comments/<uuid:comment_uuid>/sub-comments/<uuid:sub_comment_uuid>/",
        views.SubCommentRetrieveUpdateDestroyAPIView.as_view(),
        name="sub-comment-detail",
    ),
]
