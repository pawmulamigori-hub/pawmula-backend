from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.urls")),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("events.urls")),
    path("api/", include("bookings.urls")),
    path("api/", include("destinations.urls")),
    path("api/", include("experiences.urls")),
    path("api/", include("gallery.urls")),
    path("api/", include("testimonials.urls")),
    path("api/", include("faqs.urls")),
    path("api/", include("stories.urls")),
    path("api/", include("mining.urls")),
    path("api/", include("site_settings.urls")),
    path("api/", include("core.urls")),
]
