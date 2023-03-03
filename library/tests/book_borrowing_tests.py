from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from borrowing.models import Borrow
from library.models import Book, Cover
from django.utils import timezone

from user.models import User

BORROWS_URL = reverse("borrow-endpoint:borrowing-list")


class ReturnBookTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpassword"
        )
        self.borrowed_book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Cover.hard,
            inventory=2,
            daily_fee=10.0,
            need_to_refill=False,
        )
        self.borrow = Borrow.objects.create(
            borrow_date=timezone.now().date(),
            expected_return=timezone.now().date() + timezone.timedelta(days=7),
            actual_return=None,
            book=self.borrowed_book,
            user=self.user,
        )

        self.BORROW_RETURN_URL = reverse(
            "borrowing-endpoint:borrowing-return-book", kwargs={"pk": self.borrow.pk}
        )

        self.client.force_authenticate(self.user)

    def test_return_book_successfully(self):
        data = {"return_book": True}
        response = self.client.post(self.BORROW_RETURN_URL, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"status": "Your book was successfully returned"}
        )
        self.borrowed_book.refresh_from_db()
        self.assertEqual(self.borrowed_book.inventory, 3)
        self.assertFalse(self.borrowed_book.need_to_refill)
        self.borrow.refresh_from_db()
        self.assertIsNotNone(self.borrow.actual_return)

    def test_return_book_already_returned(self):
        self.borrow.actual_return = timezone.now().date()
        self.borrow.save()
        data = {"return_book": True}
        response = self.client.post(self.BORROW_RETURN_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0],
            ErrorDetail(string="This book has already been returned.", code="invalid"),
        )

    def test_return_book_invalid_data(self):
        data = {"return_book": False}
        response = self.client.post(self.BORROW_RETURN_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"error": "You must check the return_book checkbox."},
        )

    def test_return_book_permission_denied(self):
        self.client.force_authenticate(user=None)
        data = {"return_book": True}
        response = self.client.post(self.BORROW_RETURN_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_return_book_wrong_user(self):
        other_user = User.objects.create_user(
            email="otheruser@test.com", password="testpassword"
        )
        self.client.force_authenticate(user=other_user)
        data = {"return_book": True}
        response = self.client.post(self.BORROW_RETURN_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0],
            ErrorDetail(string="You can`t return book which not yours", code="invalid"),
        )
