from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse

# Root view that returns API info
def root_view(request):
    return JsonResponse({
        "status": "ok",
        "service": "Pawmula API",
        "version": "1.0.0",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/",
            "auth": "/api/auth/",
            "token_refresh": "/api/token/refresh/",
            "events": "/api/events/",
            "bookings": "/api/bookings/",
            "destinations": "/api/destinations/",
            "experiences": "/api/experiences/",
            "gallery": "/api/gallery/",
            "testimonials": "/api/testimonials/",
            "faqs": "/api/faqs/",
            "stories": "/api/stories/",
            "mining": "/api/mining/",
            "site_settings": "/api/site_settings/"
        }
    })

urlpatterns = [
    path('', root_view, name='root'),  # Add this line - root endpoint
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