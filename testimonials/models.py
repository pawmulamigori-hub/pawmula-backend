import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Testimonial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=150, blank=True)
    photo_url = models.URLField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    quote = models.TextField()
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} — {self.quote[:60]}"
