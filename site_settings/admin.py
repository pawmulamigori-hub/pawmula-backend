from django.contrib import admin
from site_settings.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ["company_name", "email", "timezone"]
    search_fields = ["company_name", "email"]
