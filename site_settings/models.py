from django.db import models


class SiteSettings(models.Model):
    """
    Singleton model for site-wide settings (pk is always 1).
    Contains contact info, social links, SEO defaults, and branding.
    """
    id = models.PositiveSmallIntegerField(primary_key=True, default=1)

    company_name = models.CharField(max_length=200, default="PAWMULA.LTD")
    tagline = models.CharField(max_length=200, default="HERITAGE . KENYA")

    address = models.CharField(max_length=300, default="Migori County, Kenya")
    phone_numbers = models.JSONField(default=list, blank=True)
    email = models.EmailField(default="pawmulamigori@gmail.com")
    whatsapp_url = models.URLField(blank=True, default="https://wa.me/254702275883")

    social_links = models.JSONField(default=dict, blank=True)

    footer_description = models.TextField(
        default="Heritage tourism, artisanal gold mining experiences and community-led journeys across western Kenya."
    )
    newsletter_text = models.CharField(max_length=200, default="Stories from the field, twice a month.")

    map_embed_url = models.URLField(blank=True, default="")
    map_lat = models.DecimalField(max_digits=9, decimal_places=6, default=-0.0917)
    map_lng = models.DecimalField(max_digits=9, decimal_places=6, default=34.7680)

    seo_title = models.CharField(max_length=255, default="Pawmula Ltd -- Discover Kenya's Hidden Heritage")
    seo_description = models.TextField(
        default="Explore Kenya's hidden heritage through community-led tourism, artisanal gold mining experiences and authentic cultural journeys in Migori and Kisumu counties."
    )
    seo_og_image = models.URLField(blank=True, null=True)
    seo_author = models.CharField(max_length=150, default="Pawmula Ltd")

    default_currency = models.CharField(max_length=6, default="KES")
    timezone = models.CharField(max_length=50, default="Africa/Nairobi")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site settings"
