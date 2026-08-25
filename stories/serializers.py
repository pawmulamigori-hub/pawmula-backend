from rest_framework import serializers
from stories.models import Story


class StorySerializer(serializers.ModelSerializer):
    publishDate = serializers.DateField(source="publish_date", required=False, allow_null=True)
    coverImage = serializers.URLField(source="cover_image", required=False, allow_null=True)
    seoTitle = serializers.CharField(source="seo_title", required=False, allow_blank=True)
    seoDescription = serializers.CharField(source="seo_description", required=False, allow_blank=True)

    class Meta:
        model = Story
        fields = [
            "id", "title", "slug", "category", "excerpt", "content",
            "coverImage", "author", "location", "publishDate", "status",
            "published", "featured", "seoTitle", "seoDescription",
        ]
        read_only_fields = ["id", "slug"]
