from django.contrib import admin
from faqs.models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "display_order", "published"]
    list_filter = ["published"]
    search_fields = ["question", "answer"]
