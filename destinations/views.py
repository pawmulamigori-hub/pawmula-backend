from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from destinations.models import Destination
from destinations.serializers import DestinationSerializer
from destinations.filters import DestinationFilter
from accounts.permissions import IsContentManager
from core.audit import log_action


class DestinationViewSet(viewsets.ModelViewSet):
    serializer_class = DestinationSerializer
    queryset = Destination.objects.all()
    filterset_class = DestinationFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Destination.objects.all()
        return Destination.objects.filter(published=True)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsContentManager()]

    def perform_create(self, serializer):
        d = serializer.save()
        log_action(self.request, "created", "Destination", d.id, d.name)

    def perform_update(self, serializer):
        d = serializer.save()
        log_action(self.request, "updated", "Destination", d.id, d.name)

    def perform_destroy(self, instance):
        log_action(self.request, "archived", "Destination", instance.id, instance.name)
        instance.delete()

    @action(detail=True, methods=["post"], url_path="set-published")
    def set_published(self, request, pk=None):
        d = self.get_object()
        d.published = bool(request.data.get("published", not d.published))
        d.save(update_fields=["published"])
        log_action(request, "published" if d.published else "unpublished", "Destination", d.id, d.name)
        return Response(DestinationSerializer(d).data)

    @action(detail=True, methods=["post"], url_path="reorder")
    def reorder(self, request, pk=None):
        d = self.get_object()
        d.display_order = int(request.data.get("displayOrder", d.display_order))
        d.save(update_fields=["display_order"])
        return Response(DestinationSerializer(d).data)
