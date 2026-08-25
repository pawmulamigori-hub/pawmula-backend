from rest_framework import serializers
from destinations.models import Destination


class DestinationSerializer(serializers.ModelSerializer):
    shortDescription = serializers.CharField(source="short_description")
    fullDescription = serializers.CharField(source="full_description")
    mainImage = serializers.URLField(source="main_image", required=False, allow_null=True)
    displayOrder = serializers.IntegerField(source="display_order", required=False)
    seoTitle = serializers.CharField(source="seo_title", required=False, allow_blank=True)
    seoDescription = serializers.CharField(source="seo_description", required=False, allow_blank=True)

    class Meta:
        model = Destination
        fields = [
            "id", "name", "slug", "county", "location", "shortDescription", "fullDescription",
            "mainImage", "gallery", "video", "featured", "published", "displayOrder",
            "seoTitle", "seoDescription",
        ]
        read_only_fields = ["id", "slug"]
