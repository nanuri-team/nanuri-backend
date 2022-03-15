from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from ..models import User
from .serializers import UserSerializer


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all().order_by('created_at')
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'
