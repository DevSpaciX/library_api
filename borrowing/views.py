from django.db import transaction
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
from borrowing.serializers import BorrowSerializer, BorrowListSerializer, BorrowReturnSerializer


class MyPagination(PageNumberPagination):
    page_size = 5  # количество объектов на странице
    page_size_query_param = 'page_size'  # название GET-параметра для установки количества объектов на странице
    max_page_size = 10  # максимальное количество объектов на странице


class BorrowViewSet(ModelViewSet):
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.select_related("book", "user")
    pagination_class = MyPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")
        if user_id:
            queryset = self.queryset.filter(user_id=user_id)
        if is_active:
            queryset = self.queryset.filter(actual_return=None)
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

    @action(methods=["POST"], detail=True, url_path="return")
    def return_book(self, request, pk=None):
        borrow = get_object_or_404(Borrow, pk=pk)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data.get("return_book"):

            if borrow.actual_return is not None:
                raise ValidationError("This book has already been returned.")
            borrow.actual_return = timezone.now()
            borrow.save()
            book = borrow.book
            book.inventory += 1
            if book.inventory >= 1 and book.need_to_refill == True:
                book.need_to_refill = False
            book.save()
            return Response({"status": "Your book was successfully returned"})

        return Response({"error": "You must check the return_book checkbox."},
                        status=status.HTTP_400_BAD_REQUEST)
