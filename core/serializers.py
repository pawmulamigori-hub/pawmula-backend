from rest_framework import serializers
from core.models import AuditLogEntry, Notification, Enquiry, HomepageContent


class HomepageContentSerializer(serializers.ModelSerializer):
    heroEyebrow = serializers.CharField(source="hero_eyebrow")
    heroHeading = serializers.CharField(source="hero_heading")
    heroSubtitle = serializers.CharField(source="hero_subtitle")
    heroImage = serializers.URLField(source="hero_image", required=False, allow_null=True)
    heroVideo = serializers.URLField(source="hero_video", required=False, allow_null=True)
    primaryCtaText = serializers.CharField(source="primary_cta_text")
    primaryCtaUrl = serializers.CharField(source="primary_cta_url")
    secondaryCtaText = serializers.CharField(source="secondary_cta_text")
    secondaryCtaUrl = serializers.CharField(source="secondary_cta_url")
    featuredDestinationSlugs = serializers.JSONField(source="featured_destination_slugs", required=False)
    trustBadges = serializers.JSONField(source="trust_badges", required=False)
    aboutEyebrow = serializers.CharField(source="about_eyebrow", required=False)
    aboutTitle = serializers.CharField(source="about_title", required=False)
    aboutDescription = serializers.CharField(source="about_description", required=False)
    aboutBlocks = serializers.JSONField(source="about_blocks", required=False)
    communityStats = serializers.JSONField(source="community_stats", required=False)
    ctaTitle = serializers.CharField(source="cta_title", required=False)
    ctaSubtitle = serializers.CharField(source="cta_subtitle", required=False)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = HomepageContent
        fields = [
            "heroEyebrow", "heroHeading", "heroSubtitle", "heroImage", "heroVideo",
            "primaryCtaText", "primaryCtaUrl", "secondaryCtaText", "secondaryCtaUrl",
            "featuredDestinationSlugs", "trustBadges",
            "aboutEyebrow", "aboutTitle", "aboutDescription", "aboutBlocks",
            "communityStats", "ctaTitle", "ctaSubtitle", "updatedAt",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    relatedId = serializers.CharField(source="related_id", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "type", "title", "body", "relatedId", "read", "createdAt"]


class AuditLogSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()
    resourceId = serializers.CharField(source="resource_id", read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AuditLogEntry
        fields = ["id", "admin", "action", "resource", "resourceId", "timestamp"]

    def get_admin(self, obj):
        return obj.admin.name if obj.admin else "System"


class EnquirySerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Enquiry
        fields = ["id", "name", "email", "phone", "subject", "message", "status", "createdAt"]
        read_only_fields = ["id", "createdAt"]
