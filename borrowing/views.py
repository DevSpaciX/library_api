from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from borrowing.models import Borrow
from borrowing.serializers import (
    BorrowSerializer,
    BorrowListSerializer,
    BorrowReturnSerializer,
)


class MyPagination(PageNumberPagination):
    page_size = 5  # количество объектов на странице
    page_size_query_param = "page_size"  # название GET-параметра для установки количества объектов на странице
    max_page_size = 10  # максимальное количество объектов на странице


class BorrowViewSet(ModelViewSet):
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.select_related("book", "user")
    pagination_class = MyPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the borrows with filters"""
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")
        print(is_active)
        if user_id:
            queryset = self.queryset.filter(user_id=user_id)
        if str(is_active) == "true":
            queryset = self.queryset.filter(actual_return=None)
        if str(is_active) == "false":
            queryset = self.queryset.filter(actual_return=not None)
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user).distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowListSerializer
        if self.action == "return_book":
            return BorrowReturnSerializer
        return BorrowSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @transaction.atomic()
    @action(methods=["POST"], detail=True, url_path="return")
    def return_book(self, request, pk=None):
        """Endpoint for returning book and close the borrow"""
        borrow = get_object_or_404(Borrow, pk=pk)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data.get("return_book"):

            if borrow.actual_return is not None:
                raise ValidationError("This book has already been returned.")
            if self.request.user != borrow.user:
                raise ValidationError("You can`t return book which not yours")
            borrow.actual_return = timezone.now()
            borrow.save()
            book = borrow.book
            book.inventory += 1
            if book.inventory >= 1 and book.need_to_refill == True:
                book.need_to_refill = False
            book.save()
            return Response(
                {"status": "Your book was successfully returned"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "You must check the return_book checkbox."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "user_id",
                type=OpenApiTypes.INT,
                description="Filter borrows by user id (ex. ?user_id=2)",
            ),
            OpenApiParameter(
                "is_active",
                type=OpenApiTypes.BOOL,
                description="Filter active borrows (ex. ?is_active=True)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
