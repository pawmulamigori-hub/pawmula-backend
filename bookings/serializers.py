from rest_framework import serializers
from bookings.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    customerName = serializers.CharField(source="customer_name")
    visitDate = serializers.DateField(source="visit_date")
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id", "reference", "customerName", "phone", "email", "experiences", "events",
            "visitDate", "guests", "amount", "currency", "status", "notes", "createdAt",
        ]
        read_only_fields = ["id", "reference", "createdAt"]


class BookingStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Booking.STATUS_CHOICES)


class BookingNoteSerializer(serializers.Serializer):
    note = serializers.CharField(allow_blank=True)


class PublicBookingCreateSerializer(serializers.ModelSerializer):
    """
    Used by the PUBLIC website's booking form (not the admin) — this is the
    other end of spec section 39's "content flows admin -> Django -> Supabase
    -> public site" pipeline, and section 9's "new booking" trigger.
    """
    customerName = serializers.CharField(source="customer_name")
    visitDate = serializers.DateField(source="visit_date")

    class Meta:
        model = Booking
        fields = ["customerName", "phone", "email", "experiences", "events", "visitDate", "guests", "amount", "currency"]

    def validate(self, attrs):
        if not attrs.get("experiences") and not attrs.get("events"):
            raise serializers.ValidationError("Select at least one experience or event.")
        return attrs
