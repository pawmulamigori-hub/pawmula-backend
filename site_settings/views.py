from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from site_settings.models import SiteSettings
from site_settings.serializers import SiteSettingsSerializer
from accounts.permissions import IsContentManager
from core.audit import log_action

from rest_framework.decorators import api_view, permission_classes


@api_view(["GET", "PATCH"])
@permission_classes([AllowAny])
def site_settings_view(request):
    """
    Public GET for site-wide settings (contact info, social links, SEO defaults).
    Authenticated PATCH requires content-manager role.
    """
    obj = SiteSettings.get_solo()

    if request.method == "GET":
        return Response(SiteSettingsSerializer(obj).data)

    if not request.user.is_authenticated or not IsContentManager().has_permission(request, None):
        return Response({"detail": "Authentication required."}, status=401)

    serializer = SiteSettingsSerializer(obj, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    log_action(request, "updated", "Site Settings", obj.pk, "Site-wide settings")
    return Response(SiteSettingsSerializer(obj).data)
