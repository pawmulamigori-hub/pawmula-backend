from django.contrib import admin
from gallery.models import GalleryItem


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "file_type", "featured", "published", "created_at"]
    list_filter = ["category", "file_type", "featured", "published"]
    search_fields = ["title", "caption"]
