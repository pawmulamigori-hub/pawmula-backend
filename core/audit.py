from core.models import AuditLogEntry


def log_action(request, action, resource, resource_id, resource_label=""):
    """Call from any mutating view. Spec section 31."""
    admin = getattr(request, "user", None)
    if admin is not None and not getattr(admin, "is_authenticated", False):
        admin = None
    ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip() or request.META.get("REMOTE_ADDR")
    AuditLogEntry.objects.create(
        admin=admin,
        action=action,
        resource=resource,
        resource_id=str(resource_id),
        resource_label=resource_label,
        ip_address=ip or None,
    )


def notify(type_, title, body="", related_id=None):
    """Create a Notification row. Spec section 32 / 9."""
    from core.models import Notification
    return Notification.objects.create(type=type_, title=title, body=body, related_id=str(related_id) if related_id else None)
