import uuid
from django.conf import settings
from django.db import models


class AuditLogEntry(models.Model):
    """Spec section 31 — every mutating admin action is recorded."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="audit_entries"
    )
    action = models.CharField(max_length=100)          # e.g. "updated", "confirmed", "published"
    resource = models.CharField(max_length=100)          # e.g. "Event", "Booking"
    resource_id = models.CharField(max_length=100)
    resource_label = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = "Audit log entries"

    def __str__(self):
        who = self.admin.name if self.admin else "System"
        return f"{who} {self.action} {self.resource} {self.resource_label or self.resource_id}"


class Notification(models.Model):
    """Spec section 32. Created by signals in events/bookings when relevant things happen."""
    TYPE_CHOICES = [
        ("booking", "New booking"),
        ("booking_cancelled", "Booking cancelled"),
        ("enquiry", "New enquiry"),
        ("event_registration", "New event registration"),
        ("event_capacity", "Event approaching capacity"),
        ("newsletter", "New newsletter subscriber"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    related_id = models.CharField(max_length=100, blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Enquiry(models.Model):
    """Contact-form submissions from the public site (spec section 18/32)."""
    STATUS_CHOICES = [("NEW", "New"), ("READ", "Read"), ("RESOLVED", "Resolved")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} — {self.subject or 'Enquiry'}"


class HomepageContent(models.Model):
    """
    Spec sections 5, 6 & 7: hardcoded homepage hero content becomes
    admin-editable and database-backed. Singleton row (id is always 1) —
    there's only ever one homepage.
    """
    id = models.PositiveSmallIntegerField(primary_key=True, default=1)
    hero_eyebrow = models.CharField(max_length=100, default="Kenya · Community-led travel")
    hero_heading = models.CharField(max_length=200, default="Discover Kenya's Hidden Heritage")
    hero_subtitle = models.TextField(
        default="Experience unforgettable journeys through history, culture, wildlife, artisanal mining, breathtaking landscapes and authentic community stories."
    )
    hero_image = models.URLField(blank=True, null=True)
    hero_video = models.URLField(blank=True, null=True)
    primary_cta_text = models.CharField(max_length=60, default="Explore Tourism")
    primary_cta_url = models.CharField(max_length=200, default="/tourism")
    secondary_cta_text = models.CharField(max_length=60, default="Explore Mining")
    secondary_cta_url = models.CharField(max_length=200, default="/mining")

    # Featured destination slugs displayed on homepage
    featured_destination_slugs = models.JSONField(
        default=list, blank=True,
        help_text="List of destination slugs to feature on the homepage.",
    )

    # Trust / feature badges shown on homepage
    trust_badges = models.JSONField(
        default=list, blank=True,
        help_text='List of {"icon": "...", "title": "...", "text": "..."} objects.',
    )

    # About section on homepage
    about_eyebrow = models.CharField(max_length=100, default="About Pawmula")
    about_title = models.CharField(max_length=200, default="Heritage told by the people who live it")
    about_description = models.TextField(
        default="Pawmula Ltd was founded to open Kenya's hidden heritage to the world."
    )
    about_blocks = models.JSONField(
        default=list, blank=True,
        help_text='List of {"heading": "...", "paragraph": "..."} content blocks.',
    )

    # Community impact section on homepage
    community_stats = models.JSONField(
        default=list, blank=True,
        help_text='List of {"label": "...", "value": N} stat objects.',
    )

    # CTA section at bottom of homepage
    cta_title = models.CharField(max_length=200, default="Your journey into Kenya's heritage starts here")
    cta_subtitle = models.TextField(default="")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Homepage content"
        verbose_name_plural = "Homepage content"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Homepage content"
