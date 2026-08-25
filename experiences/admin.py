from django.contrib import admin
from experiences.models import Experience


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "destination", "price", "published", "featured"]
    list_filter = ["published", "featured", "category"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}
