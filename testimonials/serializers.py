from rest_framework import serializers
from testimonials.models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            "id", "name", "location", "role", "photoUrl", "rating", "quote",
            "featured", "published", "displayOrder",
        ]
        read_only_fields = ["id"]

    photoUrl = serializers.URLField(source="photo_url", required=False, allow_null=True)
    displayOrder = serializers.IntegerField(source="display_order", required=False)
