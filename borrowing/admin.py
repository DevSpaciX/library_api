from django.contrib import admin

from borrowing.models import Borrow
from library.models import Book

# Register your models here.
admin.site.register(Borrow)
