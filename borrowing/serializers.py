import stripe
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from borrowing.models import Borrow
from library.models import Book
from library_core import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

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

            # Создаем новый заказ
            order = super().create(validated_data)

            # Создаем платеж в Stripe
            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(book_update.daily_fee * 100),  # Сумма в центах
                    currency="usd",
                    payment_method_types=["card"]
                )

                # Обновляем заказ с идентификатором платежа Stripe
                order.stripe_payment_id = payment_intent.id
                order.save()

                # Возвращаем информацию о платеже для передачи на клиент
                return {"client_secret": payment_intent.client_secret}

            except stripe.error.CardError as e:
                # Обработка ошибок Stripe
                error = e.error
                return {"error": error.message}

        else:
            raise serializers.ValidationError("Книга недоступна")

class BorrowListSerializer(BorrowSerializer):
    book = serializers.CharField(source="book.title")
    user = serializers.CharField(source="user.email")
    class Meta:
        model = Borrow
        fields = ("__all__")


class BorrowReturnSerializer(BorrowSerializer):
    return_book = serializers.BooleanField(default=False)
    class Meta:
        model = Borrow
        fields = ("return_book",)

