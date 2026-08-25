from rest_framework import serializers
from site_settings.models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source="company_name", required=False)
    phoneNumbers = serializers.JSONField(source="phone_numbers", required=False)
    socialLinks = serializers.JSONField(source="social_links", required=False)
    footerDescription = serializers.CharField(source="footer_description", required=False)
    newsletterText = serializers.CharField(source="newsletter_text", required=False)
    mapEmbedUrl = serializers.URLField(source="map_embed_url", required=False, allow_blank=True, allow_null=True)
    mapLat = serializers.DecimalField(source="map_lat", max_digits=9, decimal_places=6, required=False)
    mapLng = serializers.DecimalField(source="map_lng", max_digits=9, decimal_places=6, required=False)
    seoTitle = serializers.CharField(source="seo_title", required=False)
    seoDescription = serializers.CharField(source="seo_description", required=False)
    seoOgImage = serializers.URLField(source="seo_og_image", required=False, allow_null=True)
    seoAuthor = serializers.CharField(source="seo_author", required=False)
    defaultCurrency = serializers.CharField(source="default_currency", required=False)

    class Meta:
        model = SiteSettings
        fields = [
            "id", "companyName", "tagline", "address", "phoneNumbers", "email",
            "whatsappUrl", "socialLinks", "footerDescription", "newsletterText",
            "mapEmbedUrl", "mapLat", "mapLng",
            "seoTitle", "seoDescription", "seoOgImage", "seoAuthor",
            "defaultCurrency", "timezone", "updatedAt",
        ]
        read_only_fields = ["id"]

    whatsappUrl = serializers.URLField(source="whatsapp_url", required=False, allow_blank=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
