from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from faqs.models import FAQ
from faqs.serializers import FAQSerializer
from faqs.filters import FAQFilter
from accounts.permissions import IsContentManager
from core.audit import log_action


class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer
    filterset_class = FAQFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return FAQ.objects.all()
        return FAQ.objects.filter(published=True)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsContentManager()]

    def perform_create(self, serializer):
        faq = serializer.save()
        log_action(self.request, "created", "FAQ", faq.id, faq.question[:80])

    def perform_update(self, serializer):
        faq = serializer.save()
        log_action(self.request, "updated", "FAQ", faq.id, faq.question[:80])

    def perform_destroy(self, instance):
        log_action(self.request, "archived", "FAQ", instance.id, instance.question[:80])
        instance.delete()

    @action(detail=True, methods=["post"], url_path="set-published")
    def set_published(self, request, pk=None):
        faq = self.get_object()
        faq.published = bool(request.data.get("published", not faq.published))
        faq.save(update_fields=["published"])
        log_action(request, "published" if faq.published else "unpublished", "FAQ", faq.id, faq.question[:80])
        return Response(FAQSerializer(faq).data)

    @action(detail=True, methods=["post"], url_path="reorder")
    def reorder(self, request, pk=None):
        faq = self.get_object()
        faq.display_order = int(request.data.get("displayOrder", faq.display_order))
        faq.save(update_fields=["display_order"])
        return Response(FAQSerializer(faq).data)
