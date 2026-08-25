from rest_framework import serializers
from mining.models import MiningStage, MinerProfile


class MiningStageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.URLField(source="image_url", required=False, allow_null=True)
    safetyInfo = serializers.CharField(source="safety_info", required=False, allow_blank=True)
    displayOrder = serializers.IntegerField(source="display_order", required=False)

    class Meta:
        model = MiningStage
        fields = [
            "id", "name", "description", "equipment", "safetyInfo", "role",
            "imageUrl", "displayOrder", "published",
        ]
        read_only_fields = ["id"]


class MinerProfileSerializer(serializers.ModelSerializer):
    imageUrl = serializers.URLField(source="image_url", required=False, allow_null=True)
    yearsActive = serializers.IntegerField(source="years_active", required=False)
    displayOrder = serializers.IntegerField(source="display_order", required=False)

    class Meta:
        model = MinerProfile
        fields = [
            "id", "name", "imageUrl", "yearsActive", "story", "quote",
            "featured", "published", "displayOrder",
        ]
        read_only_fields = ["id"]
