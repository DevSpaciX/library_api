from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from library.views import BookViewSet
from rest_framework.authtoken import views
from user.views import CreateUserView, ManageUserView

urlpatterns = [
    path('', CreateUserView.as_view(), name="register"),
    path("login/", views.obtain_auth_token, name="token"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageUserView.as_view(), name="manage")
]

app_name = "user"