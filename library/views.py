from datetime import date
from typing import List

from rest_framework.permissions import IsAdminUser, AllowAny, BasePermission
from rest_framework.viewsets import ModelViewSet

from library.models import Book
from library.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.filter(need_to_refill=False)

    def get_permissions(self) -> List[BasePermission]:
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
