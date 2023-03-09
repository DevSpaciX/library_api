from django.urls import path, include
from rest_framework.routers import SimpleRouter
from library.views import BookViewSet

router = SimpleRouter()
router.register("books", BookViewSet, basename="books")
urlpatterns = router.urls

app_name = "books-endpoint"
