import uuid
from django.db import models


class MiningStage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField()
    equipment = models.TextField(blank=True)
    safety_info = models.TextField(blank=True)
    role = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order"]
        verbose_name = "Mining Stage"
        verbose_name_plural = "Mining Stages"

    def __str__(self):
        return self.name


class MinerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    image_url = models.URLField(blank=True, null=True)
    years_active = models.PositiveIntegerField(default=0)
    story = models.TextField()
    quote = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Miner Profile"
        verbose_name_plural = "Miner Profiles"

    def __str__(self):
        return self.name
