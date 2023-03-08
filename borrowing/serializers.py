import asyncio
from typing import Dict, Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowing.models import Borrow
from borrowing.telegram_alert import send_message_to_channel
from library.models import Book


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ("expected_return", "book")

    def create(self, validated_data: Dict[str, Any]) -> Borrow:
        book_update = Book.objects.get(title=validated_data["book"])
        if book_update.inventory > 0:
            book_update.inventory -= 1
            book_update.clean_inventory()
            book_update.save()
            asyncio.run(
                send_message_to_channel(
                    text=f"{validated_data['user']} just borrowed {validated_data['book']} and will return it {validated_data['expected_return']}"
                )
            )
            return super().create(validated_data)
        raise ValidationError("This book is sold out")


class BorrowListSerializer(BorrowSerializer):
    book = serializers.CharField(source="book.title")
    user = serializers.CharField(source="user.email")

    class Meta:
        model = Borrow
        fields = "__all__"


class BorrowDetailSerializer(BorrowSerializer):
    book = serializers.CharField(source="book.title")
    user = serializers.CharField(source="user.email")

    class Meta:
        model = Borrow
        fields = "__all__"


class BorrowReturnSerializer(BorrowSerializer):
    class Meta:
        model = Borrow
        fields = ()
