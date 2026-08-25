import uuid
import random
from django.db import models


def generate_reference():
    return f"PWM-{random.randint(1000, 9999)}"


class Booking(models.Model):
    """
    Spec section 10: a visitor can select MULTIPLE experiences/events in
    ONE booking. experiences/events are stored as simple string lists here
    (names as booked) until the Experience/Event catalog is fully wired to
    a proper M2M — the admin only needs to display and act on them, per spec.
    """
    STATUS_CHOICES = [
        ("PENDING", "Pending"), ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"), ("COMPLETED", "Completed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=20, unique=True, default=generate_reference)
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    experiences = models.JSONField(default=list, blank=True)  # ["Gold Mining Experience", ...]
    events = models.JSONField(default=list, blank=True)
    visit_date = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=6, default="KES")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} — {self.customer_name}"
