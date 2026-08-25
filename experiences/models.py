import uuid
from django.utils.text import slugify
from django.db import models


class Experience(models.Model):
    CATEGORY_CHOICES = [
        ("Tourism", "Tourism"), ("Heritage", "Heritage"), ("Mining", "Mining"),
        ("Adventure", "Adventure"), ("Culture", "Culture"), ("Community", "Community"),
        ("Nature", "Nature"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    destination = models.ForeignKey(
        "destinations.Destination", on_delete=models.SET_NULL, null=True, blank=True, related_name="experiences"
    )
    description = models.TextField()
    duration = models.CharField(max_length=100, blank=True)  # e.g. "Half day", "3 hours"
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=6, default="KES")
    max_guests = models.PositiveIntegerField(default=10)
    images = models.JSONField(default=list, blank=True)
    video = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug, i = base, 1
            while Experience.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
