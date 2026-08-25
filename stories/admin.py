from django.contrib import admin
from stories.models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "published", "featured", "publish_date"]
    list_filter = ["status", "published", "featured", "category"]
    search_fields = ["title", "excerpt", "author"]
    prepopulated_fields = {"slug": ["title"]}
