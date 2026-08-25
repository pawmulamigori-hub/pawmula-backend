from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.models import AuditLogEntry, Notification, Enquiry, HomepageContent
from core.serializers import NotificationSerializer, AuditLogSerializer, EnquirySerializer, HomepageContentSerializer
from core.storage import upload_file, SupabaseStorageError
from bookings.models import Booking
from events.models import Event
from destinations.models import Destination
from experiences.models import Experience
from accounts.permissions import IsContentManager
from core.audit import log_action


class NotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    pagination_class = None  # frontend's notificationsApi.list() expects a flat array

    @action(detail=True, methods=["post"], url_path="read")
    def mark_read(self, request, pk=None):
        n = self.get_object()
        n.read = True
        n.save(update_fields=["read"])
        return Response({"ok": True})

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        Notification.objects.filter(read=False).update(read=True)
        return Response({"ok": True})


class AuditLogViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AuditLogSerializer
    queryset = AuditLogEntry.objects.all()[:200]
    pagination_class = None  # frontend's auditApi.list() expects a flat array


class EnquiryViewSet(viewsets.ModelViewSet):
    """Spec sections 18/32 — contact-form submissions ('Messages')."""
    permission_classes = [IsAuthenticated]
    serializer_class = EnquirySerializer
    queryset = Enquiry.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]


@api_view(["POST"])
@permission_classes([AllowAny])
def public_submit_enquiry(request):
    """Public endpoint for the contact form. No auth required."""
    serializer = EnquirySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    enquiry = serializer.save()
    notify("enquiry", f"New enquiry from {enquiry.name}", enquiry.subject or "Contact form", enquiry.id)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    from stories.models import Story
    total_bookings = Booking.objects.count()
    pending = Booking.objects.filter(status="PENDING").count()
    confirmed = Booking.objects.filter(status="CONFIRMED").count()
    upcoming_events = Event.objects.filter(status__in=["PUBLISHED", "FULL"]).count()
    published_stories = Story.objects.filter(published=True).count()
    return Response({
        "totalBookings": total_bookings,
        "pendingBookings": pending,
        "confirmedBookings": confirmed,
        "upcomingEvents": upcoming_events,
        "totalExperiences": Experience.objects.filter(published=True).count(),
        "totalDestinations": Destination.objects.filter(published=True).count(),
        "publishedStories": published_stories,
        "websiteEnquiries": Enquiry.objects.filter(status="NEW").count(),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_bookings_over_time(request):
    since = timezone.now() - timedelta(days=7)
    qs = (
        Booking.objects.filter(created_at__gte=since)
        .extra(select={"day": "date(created_at)"})
        .values("day")
        .annotate(bookings=Count("id"))
        .order_by("day")
    )
    return Response([{"date": row["day"], "bookings": row["bookings"]} for row in qs])


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def media_upload(request):
    """
    Spec section 27's upload flow. Accepts multipart form data:
      - file: the image/video
      - category: folder prefix, e.g. "events", "destinations", "gallery"
    Returns {"url": "...", "path": "..."} — the frontend saves the URL
    onto the relevant record (event.coverImage, destination.mainImage, etc.)
    """
    file_obj = request.FILES.get("file")
    if not file_obj:
        return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

    category = request.data.get("category", "general")
    try:
        result = upload_file(file_obj, category=category)
    except SupabaseStorageError as e:
        return Response({"detail": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(result, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH"])
@permission_classes([AllowAny])
def homepage_content(request):
    """
    Spec sections 5/6/7/39's core pipeline for the hero section:
    GET is public/unauthenticated — the PUBLIC pawmula-frontend site calls
    this directly, no admin login needed, so hero content is never
    hardcoded in React again. PATCH requires content-manager auth.
    """
    obj = HomepageContent.get_solo()

    if request.method == "GET":
        return Response(HomepageContentSerializer(obj).data)

    if not request.user.is_authenticated or not IsContentManager().has_permission(request, None):
        return Response({"detail": "Authentication required to edit homepage content."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = HomepageContentSerializer(obj, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    log_action(request, "updated", "Homepage Content", obj.pk, "Hero section")
    return Response(HomepageContentSerializer(obj).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_popular_experiences(request):
    from collections import Counter
    counter = Counter()
    for exp_list in Booking.objects.values_list("experiences", flat=True):
        counter.update(exp_list or [])
    top = counter.most_common(5)
    return Response([{"name": name, "bookings": count} for name, count in top])
