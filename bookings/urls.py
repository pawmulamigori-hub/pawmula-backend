from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookings.views import BookingViewSet, public_create_booking

router = DefaultRouter()
router.register("bookings", BookingViewSet, basename="bookings")

urlpatterns = [
    path("public/bookings/", public_create_booking),  # consumed by the PUBLIC site
    path("", include(router.urls)),
]
