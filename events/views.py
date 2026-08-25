from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from events.models import Event
from events.serializers import EventSerializer, EventStatusSerializer
from events.filters import EventFilter
from accounts.permissions import IsEventManager
from core.audit import log_action


class EventViewSet(viewsets.ModelViewSet):
    """
    Backs the entire src/pages/events/ module of the React admin.
    URL prefix: /api/events/
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filterset_class = EventFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Event.objects.all()
        return Event.objects.filter(published=True)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsEventManager()]

    def perform_create(self, serializer):
        event = serializer.save()
        log_action(self.request, "created", "Event", event.id, event.name)

    def perform_update(self, serializer):
        event = serializer.save()
        log_action(self.request, "updated", "Event", event.id, event.name)

    def perform_destroy(self, instance):
        log_action(self.request, "archived", "Event", instance.id, instance.name)
        instance.delete()

    @action(detail=True, methods=["post"], url_path="set-status")
    def set_status(self, request, pk=None):
        event = self.get_object()
        serializer = EventStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data["status"]
        event.status = new_status
        event.published = new_status == "PUBLISHED"
        event.save(update_fields=["status", "published"])
        log_action(
            request,
            "published" if new_status == "PUBLISHED" else f"set status to {new_status} on",
            "Event", event.id, event.name,
        )
        return Response(EventSerializer(event).data)

    @action(detail=True, methods=["post"], url_path="duplicate")
    def duplicate(self, request, pk=None):
        event = self.get_object()
        event.pk = None
        event.id = None
        event.name = f"{event.name} (Copy)"
        event.slug = ""
        event.status = "DRAFT"
        event.published = False
        event.registered_count = 0
        event.save()
        log_action(request, "duplicated", "Event", event.id, event.name)
        return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
