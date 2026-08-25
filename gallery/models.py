import uuid
from django.db import models


class GalleryItem(models.Model):
    """Spec section 15 — media library backed by Supabase Storage."""
    TYPE_CHOICES = [("image", "Image"), ("video", "Video")]
    CATEGORY_CHOICES = [
        ("Tourism", "Tourism"), ("Mining", "Mining"), ("Heritage", "Heritage"),
        ("Events", "Events"), ("Community", "Community"), ("Nature", "Nature"), ("Culture", "Culture"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_url = models.URLField()  # Supabase Storage public URL
    file_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="image")
    title = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=300, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or self.file_url.split("/")[-1]
