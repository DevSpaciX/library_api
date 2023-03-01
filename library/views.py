from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from library.models import Book
from library.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

