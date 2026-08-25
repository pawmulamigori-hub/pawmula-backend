from rest_framework import serializers
from gallery.models import GalleryItem


class GalleryItemSerializer(serializers.ModelSerializer):
    fileUrl = serializers.URLField(source="file_url")
    fileType = serializers.ChoiceField(source="file_type", choices=GalleryItem.TYPE_CHOICES)
    altText = serializers.CharField(source="alt_text", required=False, allow_blank=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = GalleryItem
        fields = [
            "id", "fileUrl", "fileType", "title", "caption", "altText",
            "category", "featured", "published", "createdAt",
        ]
        read_only_fields = ["id", "createdAt"]
