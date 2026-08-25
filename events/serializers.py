from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    # camelCase aliases so the React admin needs zero field-mapping code —
    # it's already written against these exact names in mockServer.js.
    shortDescription = serializers.CharField(source="short_description")
    coverImage = serializers.URLField(source="cover_image", required=False, allow_null=True)
    startTime = serializers.TimeField(source="start_time")
    endTime = serializers.TimeField(source="end_time")
    maxCapacity = serializers.IntegerField(source="max_capacity")
    registeredCount = serializers.IntegerField(source="registered_count", read_only=True)
    registrationDeadline = serializers.DateField(source="registration_deadline")

    class Meta:
        model = Event
        fields = [
            "id", "name", "slug", "category", "description", "shortDescription",
            "coverImage", "gallery", "date", "startTime", "endTime", "location", "county",
            "price", "currency", "maxCapacity", "registeredCount", "registrationDeadline",
            "status", "featured", "published",
        ]
        read_only_fields = ["id", "slug", "registeredCount", "published"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price can't be negative.")
        return value

    def validate_maxCapacity(self, value):
        if value < 1:
            raise serializers.ValidationError("Capacity must be at least 1.")
        return value


class EventStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Event.STATUS_CHOICES)
