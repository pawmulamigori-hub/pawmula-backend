from django.contrib import admin
from events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "date", "status", "registered_count", "max_capacity", "featured"]
    list_filter = ["status", "category", "featured"]
    search_fields = ["name", "location"]
    prepopulated_fields = {"slug": ["name"]}
