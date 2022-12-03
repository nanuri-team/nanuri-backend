from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from ..models import User


class UserListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().order_by("created_at")
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = self.queryset
        if nickname := self.request.query_params.get("nickname", None):
            queryset = queryset.filter(nickname=nickname)
        return queryset


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "uuid"
