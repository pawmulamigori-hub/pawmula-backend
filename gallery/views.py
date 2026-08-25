from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from gallery.models import GalleryItem
from gallery.serializers import GalleryItemSerializer
from gallery.filters import GalleryItemFilter
from accounts.permissions import IsContentManager
from core.audit import log_action


class GalleryItemViewSet(viewsets.ModelViewSet):
    serializer_class = GalleryItemSerializer
    queryset = GalleryItem.objects.all()
    filterset_class = GalleryItemFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return GalleryItem.objects.all()
        return GalleryItem.objects.filter(published=True)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsContentManager()]

    def perform_create(self, serializer):
        item = serializer.save()
        log_action(self.request, "uploaded", "Gallery Item", item.id, item.title or item.category)

    def perform_update(self, serializer):
        item = serializer.save()
        log_action(self.request, "updated", "Gallery Item", item.id, item.title or item.category)

    def perform_destroy(self, instance):
        log_action(self.request, "deleted", "Gallery Item", instance.id, instance.title or instance.category)
        instance.delete()
