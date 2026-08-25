from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import login_view, me_view, logout_view, AdminUserViewSet

router = DefaultRouter()
router.register("users", AdminUserViewSet, basename="users")

urlpatterns = [
    path("auth/login/", login_view),
    path("auth/me/", me_view),
    path("auth/logout/", logout_view),
    path("", include(router.urls)),
]
