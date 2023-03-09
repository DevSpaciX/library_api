from rest_framework.routers import SimpleRouter
from borrowing.views import BorrowViewSet

router = SimpleRouter()
router.register("borrowings", BorrowViewSet, basename="borrowing")
urlpatterns = router.urls

app_name = "borrow-endpoint"
