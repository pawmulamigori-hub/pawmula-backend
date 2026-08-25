from django.contrib.auth import authenticate
from rest_framework import generics, status, mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import AdminUser
from accounts.serializers import AdminUserSerializer, InviteAdminSerializer
from accounts.permissions import IsSuperAdmin
from core.audit import log_action


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email", "").strip().lower()
    password = request.data.get("password", "")
    user = authenticate(request, username=email, password=password)
    if user is None or not user.active:
        return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        "token": str(refresh.access_token),
        "refresh": str(refresh),
        "user": AdminUserSerializer(user).data,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response(AdminUserSerializer(request.user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # Stateless JWT — nothing to invalidate server-side without a
    # blocklist app; the frontend simply discards its token.
    return Response({"ok": True})


from rest_framework.decorators import action


class AdminUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    queryset = AdminUser.objects.all().order_by("name")
    serializer_class = AdminUserSerializer
    pagination_class = None  # frontend's usersApi.list() expects a flat array

    @action(detail=False, methods=["post"], url_path="invite")
    def invite(self, request):
        serializer = InviteAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        log_action(request, "invited", "Admin User", user.id, user.email)
        return Response(AdminUserSerializer(user).data, status=status.HTTP_201_CREATED)
