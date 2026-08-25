import uuid
from django.utils.text import slugify
from django.db import models


class Event(models.Model):
    CATEGORY_CHOICES = [
        ("Tourism", "Tourism"), ("Heritage", "Heritage"), ("Mining", "Mining"),
        ("Adventure", "Adventure"), ("Culture", "Culture"), ("Community", "Community"),
        ("Nature", "Nature"),
    ]
    STATUS_CHOICES = [
        ("DRAFT", "Draft"), ("PUBLISHED", "Published"), ("FULL", "Full"),
        ("CANCELLED", "Cancelled"), ("COMPLETED", "Completed"), ("ARCHIVED", "Archived"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    cover_image = models.URLField(blank=True, null=True)  # Supabase Storage public URL
    gallery = models.JSONField(default=list, blank=True)  # list of Supabase Storage URLs

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    county = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=6, default="KES")
    max_capacity = models.PositiveIntegerField(default=20)
    registered_count = models.PositiveIntegerField(default=0)
    registration_deadline = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug, i = base, 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        # Auto-flip to FULL when capacity is reached, mirrors spec section 8 statuses
        if self.status == "PUBLISHED" and self.registered_count >= self.max_capacity:
            self.status = "FULL"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
