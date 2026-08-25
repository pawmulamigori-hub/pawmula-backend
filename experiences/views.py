from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from experiences.models import Experience
from experiences.serializers import ExperienceSerializer
from experiences.filters import ExperienceFilter
from accounts.permissions import IsContentManager
from core.audit import log_action


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.select_related("destination").all()
    filterset_class = ExperienceFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Experience.objects.select_related("destination").all()
        return Experience.objects.select_related("destination").filter(published=True)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsContentManager()]

    def perform_create(self, serializer):
        e = serializer.save()
        log_action(self.request, "created", "Experience", e.id, e.name)

    def perform_update(self, serializer):
        e = serializer.save()
        log_action(self.request, "updated", "Experience", e.id, e.name)

    def perform_destroy(self, instance):
        log_action(self.request, "archived", "Experience", instance.id, instance.name)
        instance.delete()

    @action(detail=True, methods=["post"], url_path="set-published")
    def set_published(self, request, pk=None):
        e = self.get_object()
        e.published = bool(request.data.get("published", not e.published))
        e.save(update_fields=["published"])
        log_action(request, "published" if e.published else "unpublished", "Experience", e.id, e.name)
        return Response(ExperienceSerializer(e).data)
