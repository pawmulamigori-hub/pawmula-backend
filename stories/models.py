import uuid
from django.utils.text import slugify
from django.db import models


class Story(models.Model):
    CATEGORY_CHOICES = [
        ("Tourism", "Tourism"), ("Heritage", "Heritage"), ("Mining", "Mining"),
        ("Adventure", "Adventure"), ("Culture", "Culture"), ("Community", "Community"),
        ("Nature", "Nature"), ("Oral History", "Oral History"), ("Guide", "Guide"),
    ]
    STATUS_CHOICES = [
        ("DRAFT", "Draft"), ("PUBLISHED", "Published"), ("ARCHIVED", "Archived"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    excerpt = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    cover_image = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=255, blank=True)
    publish_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publish_date", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug, i = base, 1
            while Story.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        if self.status == "PUBLISHED":
            self.published = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
