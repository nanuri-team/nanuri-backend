from django.urls import path

from .views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView

app_name = 'nanuri.posts'

urlpatterns = [
    path('', PostListCreateAPIView.as_view(), name='list'),
    path('<uuid:uuid>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
]
