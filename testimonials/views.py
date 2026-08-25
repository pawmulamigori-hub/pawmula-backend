from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from testimonials.models import Testimonial
from testimonials.serializers import TestimonialSerializer
from testimonials.filters import TestimonialFilter
from accounts.permissions import IsContentManager
from core.audit import log_action


class TestimonialViewSet(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    filterset_class = TestimonialFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Testimonial.objects.all()
        return Testimonial.objects.filter(published=True)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsContentManager()]

    def perform_create(self, serializer):
        t = serializer.save()
        log_action(self.request, "created", "Testimonial", t.id, t.name)

    def perform_update(self, serializer):
        t = serializer.save()
        log_action(self.request, "updated", "Testimonial", t.id, t.name)

    def perform_destroy(self, instance):
        log_action(self.request, "archived", "Testimonial", instance.id, instance.name)
        instance.delete()

    @action(detail=True, methods=["post"], url_path="set-published")
    def set_published(self, request, pk=None):
        t = self.get_object()
        t.published = bool(request.data.get("published", not t.published))
        t.save(update_fields=["published"])
        log_action(request, "published" if t.published else "unpublished", "Testimonial", t.id, t.name)
        return Response(TestimonialSerializer(t).data)

    @action(detail=True, methods=["post"], url_path="reorder")
    def reorder(self, request, pk=None):
        t = self.get_object()
        t.display_order = int(request.data.get("displayOrder", t.display_order))
        t.save(update_fields=["display_order"])
        return Response(TestimonialSerializer(t).data)
