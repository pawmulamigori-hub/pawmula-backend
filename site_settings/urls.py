from django.urls import path
from site_settings.views import site_settings_view

urlpatterns = [
    path("website/settings/", site_settings_view),
]
