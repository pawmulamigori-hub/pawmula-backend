from django.contrib import admin
from bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["reference", "customer_name", "visit_date", "guests", "amount", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["reference", "customer_name", "email"]
