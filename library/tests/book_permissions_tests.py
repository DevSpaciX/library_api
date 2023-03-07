from django.template.defaultfilters import lower
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from library.models import Book, Cover

BOOK_URL = reverse("books-endpoint:books-list")


client = APIClient()


class BookViewSetTestCase(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Cover.soft,
            inventory=5,
            daily_fee=1.99,
            need_to_refill=False,
        )

    def test_permissions_for_list(self):
        url = BOOK_URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permissions_for_create(self):
        url = BOOK_URL
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": Cover.hard,
            "inventory": 10,
            "daily_fee": 2.99,
            "need_to_refill": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissions_for_retrieve(self):
        url = reverse("books-endpoint:books-detail", kwargs={"pk": self.book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permissions_for_update(self):
        url = reverse("books-endpoint:books-detail", kwargs={"pk": self.book.id})
        data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "cover": Cover.hard,
            "inventory": 10,
            "daily_fee": 2.99,
            "need_to_refill": False,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissions_for_partial_update(self):
        url = reverse("books-endpoint:books-detail", kwargs={"pk": self.book.id})
        data = {
            "title": "Updated Book",
            "inventory": 10,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissions_for_delete(self):
        url = reverse("books-endpoint:books-detail", kwargs={"pk": self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_queryset(self):
        url = BOOK_URL
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.book.title)
        self.assertEqual(response.data[0]["inventory"], self.book.inventory)
        self.assertEqual(lower(str(response.data[0]["cover"])), self.book.cover.name)
        self.assertEqual(response.data[0]["daily_fee"], str(self.book.daily_fee))
