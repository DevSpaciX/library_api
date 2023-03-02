from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from borrowing.models import Borrow
from library.models import Book


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ("expected_return", "book")

    def create(self, validated_data):
        book_update = Book.objects.get(title=validated_data["book"])
        if book_update.inventory > 0:
            book_update.inventory -= 1
            book_update.clean_inventory()
            book_update.save()
            return super().create(validated_data)


class BorrowListSerializer(BorrowSerializer):
    book = serializers.CharField(source="book.title")
    user = serializers.CharField(source="user.email")
    class Meta:
        model = Borrow
        fields = ("id","borrow_date","expected_return","book","user")

