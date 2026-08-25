from django.contrib import admin
from testimonials.models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["name", "rating", "featured", "published", "display_order"]
    list_filter = ["published", "featured", "rating"]
    search_fields = ["name", "quote"]
