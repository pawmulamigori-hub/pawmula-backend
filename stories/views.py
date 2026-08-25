from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from stories.models import Story
from stories.serializers import StorySerializer
from stories.filters import StoryFilter
from accounts.permissions import IsEventManager
from core.audit import log_action


class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    filterset_class = StoryFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Story.objects.all()
        return Story.objects.filter(published=True)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsEventManager()]

    def perform_create(self, serializer):
        s = serializer.save()
        log_action(self.request, "created", "Story", s.id, s.title)

    def perform_update(self, serializer):
        s = serializer.save()
        log_action(self.request, "updated", "Story", s.id, s.title)

    def perform_destroy(self, instance):
        log_action(self.request, "archived", "Story", instance.id, instance.title)
        instance.delete()

    @action(detail=True, methods=["post"], url_path="set-published")
    def set_published(self, request, pk=None):
        s = self.get_object()
        new_val = bool(request.data.get("published", not s.published))
        s.published = new_val
        s.status = "PUBLISHED" if new_val else "DRAFT"
        s.save(update_fields=["published", "status"])
        log_action(request, "published" if s.published else "unpublished", "Story", s.id, s.title)
        return Response(StorySerializer(s).data)
