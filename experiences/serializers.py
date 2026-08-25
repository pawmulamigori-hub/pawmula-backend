from rest_framework import serializers
from experiences.models import Experience
from destinations.models import Destination


class ExperienceSerializer(serializers.ModelSerializer):
    maxGuests = serializers.IntegerField(source="max_guests")
    destinationId = serializers.PrimaryKeyRelatedField(
        source="destination", queryset=Destination.objects.all(), required=False, allow_null=True,
    )
    destinationName = serializers.CharField(source="destination.name", read_only=True, default=None)
    seoTitle = serializers.CharField(source="seo_title", required=False, allow_blank=True)
    seoDescription = serializers.CharField(source="seo_description", required=False, allow_blank=True)

    class Meta:
        model = Experience
        fields = [
            "id", "name", "slug", "category", "destinationId", "destinationName", "description",
            "duration", "price", "currency", "maxGuests", "images", "video", "featured", "published",
            "seoTitle", "seoDescription",
        ]
        read_only_fields = ["id", "slug"]
