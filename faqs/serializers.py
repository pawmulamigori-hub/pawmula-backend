from rest_framework import serializers
from faqs.models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    displayOrder = serializers.IntegerField(source="display_order", required=False)

    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "displayOrder", "published"]
        read_only_fields = ["id"]
