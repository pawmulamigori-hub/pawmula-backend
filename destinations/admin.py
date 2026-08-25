from django.contrib import admin
from destinations.models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ["name", "county", "published", "featured", "display_order"]
    list_filter = ["published", "featured", "county"]
    search_fields = ["name", "location"]
    prepopulated_fields = {"slug": ["name"]}
