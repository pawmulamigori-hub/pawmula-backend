from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    NotificationViewSet, AuditLogViewSet, EnquiryViewSet,
    dashboard_stats, dashboard_bookings_over_time, dashboard_popular_experiences,
    media_upload, homepage_content, public_submit_enquiry,
)

router = DefaultRouter()
router.register("notifications", NotificationViewSet, basename="notifications")
router.register("audit-log", AuditLogViewSet, basename="audit-log")
router.register("messages", EnquiryViewSet, basename="messages")

urlpatterns = [
    path("dashboard/stats/", dashboard_stats),
    path("dashboard/bookings-over-time/", dashboard_bookings_over_time),
    path("dashboard/popular-experiences/", dashboard_popular_experiences),
    path("media/upload/", media_upload),
    path("website/homepage/", homepage_content),
    path("public/messages/", public_submit_enquiry),
    path("", include(router.urls)),
]
