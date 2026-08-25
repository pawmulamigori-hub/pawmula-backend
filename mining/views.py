from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from mining.models import MiningStage, MinerProfile
from mining.serializers import MiningStageSerializer, MinerProfileSerializer
from mining.filters import MiningStageFilter, MinerProfileFilter
from accounts.permissions import IsContentManager
from core.audit import log_action


class MiningStageViewSet(viewsets.ModelViewSet):
    serializer_class = MiningStageSerializer
    filterset_class = MiningStageFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MiningStage.objects.all()
        return MiningStage.objects.filter(published=True)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsContentManager()]

    def perform_create(self, serializer):
        s = serializer.save()
        log_action(self.request, "created", "Mining Stage", s.id, s.name)

    def perform_update(self, serializer):
        s = serializer.save()
        log_action(self.request, "updated", "Mining Stage", s.id, s.name)

    def perform_destroy(self, instance):
        log_action(self.request, "archived", "Mining Stage", instance.id, instance.name)
        instance.delete()

    @action(detail=True, methods=["post"], url_path="set-published")
    def set_published(self, request, pk=None):
        s = self.get_object()
        s.published = bool(request.data.get("published", not s.published))
        s.save(update_fields=["published"])
        log_action(request, "published" if s.published else "unpublished", "Mining Stage", s.id, s.name)
        return Response(MiningStageSerializer(s).data)

    @action(detail=True, methods=["post"], url_path="reorder")
    def reorder(self, request, pk=None):
        s = self.get_object()
        s.display_order = int(request.data.get("displayOrder", s.display_order))
        s.save(update_fields=["display_order"])
        return Response(MiningStageSerializer(s).data)


class MinerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = MinerProfileSerializer
    filterset_class = MinerProfileFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MinerProfile.objects.all()
        return MinerProfile.objects.filter(published=True)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsContentManager()]

    def perform_create(self, serializer):
        m = serializer.save()
        log_action(self.request, "created", "Miner Profile", m.id, m.name)

    def perform_update(self, serializer):
        m = serializer.save()
        log_action(self.request, "updated", "Miner Profile", m.id, m.name)

    def perform_destroy(self, instance):
        log_action(self.request, "archived", "Miner Profile", instance.id, instance.name)
        instance.delete()

    @action(detail=True, methods=["post"], url_path="set-published")
    def set_published(self, request, pk=None):
        m = self.get_object()
        m.published = bool(request.data.get("published", not m.published))
        m.save(update_fields=["published"])
        log_action(request, "published" if m.published else "unpublished", "Miner Profile", m.id, m.name)
        return Response(MinerProfileSerializer(m).data)

    @action(detail=True, methods=["post"], url_path="reorder")
    def reorder(self, request, pk=None):
        m = self.get_object()
        m.display_order = int(request.data.get("displayOrder", m.display_order))
        m.save(update_fields=["display_order"])
        return Response(MinerProfileSerializer(m).data)
