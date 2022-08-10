from drf_spectacular.utils import extend_schema_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from ..models import User
from . import specs
from .serializers import UserSerializer


@extend_schema_view(**specs.users_api_specs)
class UserListCreateAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by("created_at")
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination


@extend_schema_view(**specs.user_api_specs)
class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "uuid"
