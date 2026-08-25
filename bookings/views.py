from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from bookings.models import Booking
from bookings.serializers import (
    BookingSerializer, BookingStatusSerializer, BookingNoteSerializer, PublicBookingCreateSerializer,
)
from bookings.filters import BookingFilter
from accounts.permissions import IsBookingManager
from core.audit import log_action
from core.audit import notify


class BookingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Admin-facing. URL prefix: /api/bookings/
    Bookings are created by the PUBLIC site via bookings.public_create_booking,
    never by the admin directly (spec: admin manages, visitors book).
    """
    permission_classes = [IsAuthenticated, IsBookingManager]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    filterset_class = BookingFilter

    @action(detail=True, methods=["post"], url_path="set-status")
    def set_status(self, request, pk=None):
        booking = self.get_object()
        serializer = BookingStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking.status = serializer.validated_data["status"]
        booking.save(update_fields=["status"])
        log_action(request, booking.status.lower(), "Booking", booking.id, booking.reference)
        return Response(BookingSerializer(booking).data)

    @action(detail=True, methods=["post"], url_path="notes")
    def add_note(self, request, pk=None):
        booking = self.get_object()
        serializer = BookingNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking.notes = serializer.validated_data["note"]
        booking.save(update_fields=["notes"])
        log_action(request, "added a note to", "Booking", booking.id, booking.reference)
        return Response(BookingSerializer(booking).data)


@api_view(["POST"])
@permission_classes([AllowAny])
def public_create_booking(request):
    """
    The PUBLIC website posts here (spec sections 9 & 10). No auth required —
    this is a visitor-facing endpoint, rate-limit it at the infra/CDN layer
    in production. Triggers the notification the admin dashboard polls for.
    """
    serializer = PublicBookingCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    booking = serializer.save()

    items = ", ".join((booking.experiences or []) + (booking.events or []))
    notify(
        "booking",
        "New booking received",
        f"{booking.customer_name} booked {items or 'an experience'} for {booking.guests} guests.",
        related_id=booking.id,
    )
    return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
